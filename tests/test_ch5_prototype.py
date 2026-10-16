"""Fail-closed checks for the real-asset Chapter 5 prototype, without a network."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]/'projects/youtube/001-therapy-speak/ch5-prototype'
try:
    from PIL import ImageChops
except ImportError:
    ImageChops = None


@unittest.skipIf(ImageChops is None, 'Pillow required; install ch5-prototype/requirements.txt')
class PrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('ch5_render', ROOT/'render.py')
        cls.r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.r)

    def test_captions_match_canonical_and_inherited_speech_boundaries(self):
        shots, timing = self.r.inputs()
        self.assertEqual(len(timing['sentences']),19)
        self.assertEqual(timing['sentences'][0]['start'],self.r.START)
        self.assertEqual(timing['sentences'][-1]['end'],self.r.END)
        evidence = json.loads((ROOT.parent/'visual-batch-v1/ch5-pilot-evidence-v1.json').read_text())
        for shot, source in zip(shots,evidence['units']):
            self.assertEqual(shot['speech'],[source['spoken_first_word_seconds'],source['spoken_last_word_seconds']])
        missing = [w for w in timing['words'] if not w['verified']]
        self.assertEqual([w['word'] for w in missing],['sixty','understaffing,'])
        self.assertTrue(all(w['start'] is None and w['end'] is None for w in missing))

    def test_changed_alignment_fails_closed(self):
        original = self.r.HERE
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'episode'
            shutil.copytree(ROOT.parent,root,ignore=shutil.ignore_patterns('__pycache__','outputs'))
            timing = root/'ch5-prototype/timing.json'
            data = json.loads(timing.read_text())
            data['sentences'][0]['start'] -= .2
            timing.write_text(json.dumps(data))
            self.r.HERE,self.r.EPISODE = timing.parent,root
            try:
                with self.assertRaisesRegex(ValueError,'Prototype input changed'):
                    self.r.inputs()
            finally:
                self.r.HERE,self.r.EPISODE = original,original.parent

    def test_reveals_are_supported_by_actual_word_or_sentence_edges(self):
        _,timing = self.r.inputs()
        timeline = json.loads((ROOT/'timeline.json').read_text())
        for event in timeline['events']:
            if event['basis'] == 'neutral_hold':
                continue
            if event['basis'] == 'reuse_previously_supported_scene':
                self.assertGreater(event['at_master'],648.56)
                continue
            s = next(s for s in timing['sentences'] if s['index']==event['sentence_index'])
            self.assertIn(event['supporting_quote'],s['text'])
            if event['basis'] == 'sentence_start':
                self.assertEqual(event['at_master'],s['start'])
            elif event['basis'] == 'sentence_end':
                self.assertEqual(event['at_master'],s['end'])
            else:
                word = next(w for w in timing['words'] if w['index']==event['word_index'])
                self.assertTrue(word['verified'])
                self.assertEqual(event['at_master'],word['end'])

    def test_caption_and_artwork_safe_area_and_direct_seek(self):
        _,timing = self.r.inputs()
        art = self.r.Artwork(timing)
        samples = [0,8.1,15.3,23.04,23.4,24.1,30,38.15,43.15,43.7,47,52,55,63.28,63.63,75,80.95]
        for t in samples:
            frame = art.frame(t)
            self.assertEqual(frame.size,(1920,1080))
            self.assertEqual(frame.getpixel((0,0)),(255,255,255))
            self.assertEqual(frame.getchannel('R').tobytes(),frame.getchannel('G').tobytes())
            self.assertIsNone(ImageChops.difference(frame.crop((0,864,1920,1080)),
                                                     self.r.Image.new('RGB',(1920,216),'white')).getbbox())
        direct = art.frame(63.28).tobytes()
        for t in reversed(samples):
            art.frame(t)
        self.assertEqual(direct,art.frame(63.28).tobytes())
        for s in timing['sentences']:
            self.assertLessEqual(len(art.wrap(s['text'])),2)

    def test_source_claim_not_shown_before_support(self):
        _,timing = self.r.inputs()
        art=self.r.Artwork(timing)
        art.frame(678.8-self.r.START)
        self.assertNotIn('World Health Organization',[s for s,_ in art.bounds])
        art.frame(678.91-self.r.START)
        self.assertIn('World Health Organization',[s for s,_ in art.bounds])
        art.frame(683.051-self.r.START)
        self.assertNotIn('occupational phenomenon',[s for s,_ in art.bounds])
        art.frame(683.052-self.r.START)
        self.assertIn('occupational phenomenon',[s for s,_ in art.bounds])
        art.frame(691.255-self.r.START)
        self.assertNotIn('Not classified as a medical condition',[s for s,_ in art.bounds])
        art.frame(691.256-self.r.START)
        self.assertIn('Not classified as a medical condition',[s for s,_ in art.bounds])


if __name__=='__main__':
    unittest.main()
