package com.letfate.coin;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.animation.ValueAnimator;
import android.app.Activity;
import android.content.Context;
import android.graphics.*;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.view.HapticFeedbackConstants;
import android.view.MotionEvent;
import android.view.View;
import android.view.Window;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.view.animation.DecelerateInterpolator;

import java.security.SecureRandom;
import java.util.Locale;

public class MainActivity extends Activity {

    private FateView fateView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Window window = getWindow();
        window.setStatusBarColor(Color.rgb(241, 235, 226));
        window.setNavigationBarColor(Color.rgb(241, 235, 226));

        if (android.os.Build.VERSION.SDK_INT >= 30) {
            WindowInsetsController c = window.getInsetsController();
            if (c != null) {
                c.setSystemBarsAppearance(
                        WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS
                                | WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS,
                        WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS
                                | WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS
                );
            }
        } else {
            window.getDecorView().setSystemUiVisibility(
                    View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR
            );
        }

        fateView = new FateView(this);
        setContentView(fateView);
    }

    public static final class FateView extends View {
        private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
        private final Paint stroke = new Paint(Paint.ANTI_ALIAS_FLAG);
        private final SecureRandom random = new SecureRandom();

        private final Typeface display = Typeface.create("serif", Typeface.NORMAL);
        private final Typeface displayItalic = Typeface.create("serif", Typeface.ITALIC);
        private final Typeface sans = Typeface.create("sans-serif", Typeface.NORMAL);
        private final Typeface sansMedium = Typeface.create("sans-serif-medium", Typeface.NORMAL);

        private int tosses = 0;
        private int heads = 0;
        private int tails = 0;

        private Boolean lastResult = null;
        private boolean displayHeads = true;
        private boolean pendingHeads = true;
        private boolean flipping = false;
        private float flipProgress = 0f;
        private int halfTurns = 8;

        private float downX;
        private float downY;

        private ValueAnimator animator;

        FateView(Context context) {
            super(context);
            setLayerType(View.LAYER_TYPE_SOFTWARE, null);
            setBackground(new ColorDrawable(Color.TRANSPARENT));
            setClickable(true);
        }

        private int ivory() { return Color.rgb(241, 235, 226); }
        private int ink() { return Color.rgb(18, 18, 16); }
        private int black() { return Color.rgb(12, 12, 11); }
        private int cream() { return Color.rgb(239, 229, 213); }
        private int mutedLight() { return Color.rgb(105, 100, 93); }
        private int mutedDark() { return Color.rgb(160, 151, 138); }

        private boolean darkMode() {
            return lastResult != null && !lastResult;
        }

        @Override
        protected void onDraw(Canvas canvas) {
            super.onDraw(canvas);
            int w = getWidth();
            int h = getHeight();
            if (w <= 0 || h <= 0) return;

            float s = w / 390f;
            boolean dark = darkMode();

            drawBackground(canvas, w, h, dark, s);
            drawHeader(canvas, w, h, dark, s);
            drawCoin(canvas, w, h, dark, s);
            drawResult(canvas, w, h, dark, s);
            drawFooter(canvas, w, h, dark, s);
        }

        private void drawBackground(Canvas c, int w, int h, boolean dark, float s) {
            paint.setStyle(Paint.Style.FILL);
            paint.setShader(null);
            paint.setColor(dark ? black() : ivory());
            c.drawRect(0, 0, w, h, paint);

            if (dark) {
                RadialGradient glow = new RadialGradient(
                        w * 0.52f, h * 0.42f, w * 0.78f,
                        new int[]{Color.argb(30, 202, 159, 81), Color.TRANSPARENT},
                        new float[]{0f, 1f},
                        Shader.TileMode.CLAMP
                );
                paint.setShader(glow);
                c.drawRect(0, 0, w, h, paint);
                paint.setShader(null);
            } else {
                LinearGradient light = new LinearGradient(
                        0, 0, w, h * 0.7f,
                        new int[]{
                                Color.argb(90, 255, 255, 255),
                                Color.argb(0, 255, 255, 255),
                                Color.argb(42, 203, 185, 158)
                        },
                        new float[]{0f, 0.45f, 1f},
                        Shader.TileMode.CLAMP
                );
                paint.setShader(light);
                c.drawRect(0, 0, w, h, paint);
                paint.setShader(null);

                paint.setColor(Color.argb(34, 110, 92, 70));
                c.save();
                c.rotate(-19f, w * .18f, h * .05f);
                c.drawRect(-w * .3f, h * .01f, w * .78f, h * .045f, paint);
                c.restore();
            }
        }

        private void drawHeader(Canvas c, int w, int h, boolean dark, float s) {
            int fg = dark ? cream() : ink();
            int muted = dark ? mutedDark() : mutedLight();

            paint.setShader(null);
            paint.setTypeface(sans);
            paint.setTextSize(8.2f * s);
            paint.setColor(muted);
            paint.setLetterSpacingCompat(0f);

            drawSpacedText(c, "A SMALL COIN", 16f * s, h * .058f, 1.75f * s, paint, false);
            drawSpacedText(c, "A BIGGER YOU", 16f * s, h * .077f, 1.75f * s, paint, false);

            paint.setColor(fg);
            paint.setTypeface(display);
            paint.setTextSize(54f * s);
            paint.setFakeBoldText(false);
            drawCentered(c, "LET FATE", w / 2f, h * .172f, paint);

            paint.setTypeface(displayItalic);
            paint.setTextSize(17f * s);
            paint.setColor(muted);
            drawCentered(c, "Leave it to chance.", w / 2f, h * .211f, paint);

            stroke.setStyle(Paint.Style.STROKE);
            stroke.setStrokeWidth(.7f * s);
            stroke.setColor(dark ? Color.argb(90, 225, 210, 187) : Color.argb(100, 40, 35, 28));
            c.drawLine(w * .40f, h * .238f, w * .46f, h * .238f, stroke);
            c.drawLine(w * .54f, h * .238f, w * .60f, h * .238f, stroke);

            paint.setTypeface(sans);
            paint.setTextSize(7.2f * s);
            paint.setColor(muted);
            drawSpacedCentered(c, "COIN TOSS", w / 2f, h * .2415f, 3.2f * s, paint);
        }

        private void drawCoin(Canvas c, int w, int h, boolean dark, float s) {
            float baseCy = h * .505f;
            float r = Math.min(w * .31f, h * .185f);
            float cy = baseCy;
            float scaleX = 1f;
            boolean faceHeads = displayHeads;
            float zRotation = 0f;

            if (flipping) {
                float p = flipProgress;
                cy -= 62f * s * 4f * p * (1f - p);
                float phase = p * halfTurns * (float)Math.PI;
                float cos = (float)Math.cos(phase);
                scaleX = Math.max(.055f, Math.abs(cos));
                faceHeads = cos >= 0f ? displayHeads : !displayHeads;
                zRotation = (float)Math.sin(p * Math.PI) * 5.5f;
            }

            c.save();
            c.translate(w / 2f, cy);
            c.rotate(zRotation);
            c.scale(scaleX, 1f);

            paint.setShadowLayer(26f * s, 0, 18f * s, dark ? Color.argb(150, 0, 0, 0) : Color.argb(80, 52, 37, 18));
            RadialGradient gold = new RadialGradient(
                    -r * .25f, -r * .32f, r * 1.4f,
                    new int[]{
                            Color.rgb(251, 231, 169),
                            Color.rgb(216, 177, 96),
                            Color.rgb(163, 121, 55),
                            Color.rgb(232, 194, 112)
                    },
                    new float[]{0f, .40f, .72f, 1f},
                    Shader.TileMode.CLAMP
            );
            paint.setShader(gold);
            paint.setStyle(Paint.Style.FILL);
            c.drawCircle(0, 0, r, paint);
            paint.clearShadowLayer();

            stroke.setShader(null);
            stroke.setStyle(Paint.Style.STROKE);
            stroke.setStrokeWidth(3.3f * s);
            stroke.setColor(Color.rgb(112, 78, 31));
            c.drawCircle(0, 0, r - 2.2f * s, stroke);

            stroke.setStrokeWidth(1.2f * s);
            stroke.setColor(Color.argb(210, 255, 240, 191));
            c.drawCircle(0, 0, r - 9.5f * s, stroke);

            stroke.setPathEffect(new DashPathEffect(new float[]{2.6f * s, 3.7f * s}, 0));
            stroke.setStrokeWidth(1.4f * s);
            stroke.setColor(Color.rgb(118, 81, 30));
            c.drawCircle(0, 0, r * .73f, stroke);
            stroke.setPathEffect(null);

            paint.setShader(null);
            paint.setColor(Color.rgb(91, 61, 25));

            if (faceHeads) drawHeadsFace(c, r, s);
            else drawTailsFace(c, r, s);

            drawCoinRimText(c, faceHeads ? "LET FATE DECIDE" : "GOOD THINGS TAKE TIME", r * .84f, 7.2f * s);

            c.restore();
        }

        private void drawHeadsFace(Canvas c, float r, float s) {
            paint.setStyle(Paint.Style.FILL);
            paint.setColor(Color.argb(205, 82, 54, 21));

            Path p = new Path();
            p.moveTo(-r * .24f, r * .35f);
            p.cubicTo(-r * .31f, r * .16f, -r * .30f, -r * .04f, -r * .20f, -r * .22f);
            p.cubicTo(-r * .12f, -r * .39f, r * .03f, -r * .43f, r * .11f, -r * .31f);
            p.cubicTo(r * .14f, -r * .27f, r * .12f, -r * .22f, r * .18f, -r * .19f);
            p.lineTo(r * .28f, -r * .14f);
            p.lineTo(r * .18f, -r * .08f);
            p.cubicTo(r * .14f, -r * .02f, r * .12f, r * .04f, r * .12f, r * .10f);
            p.cubicTo(r * .10f, r * .19f, r * .03f, r * .24f, -r * .03f, r * .27f);
            p.lineTo(r * .02f, r * .40f);
            p.close();
            c.drawPath(p, paint);

            stroke.setStyle(Paint.Style.STROKE);
            stroke.setStrokeWidth(1.1f * s);
            stroke.setColor(Color.argb(170, 250, 224, 157));
            Path hair = new Path();
            hair.moveTo(-r * .24f, r * .05f);
            hair.cubicTo(-r * .42f, -r * .08f, -r * .36f, -r * .38f, -r * .12f, -r * .41f);
            hair.cubicTo(-r * .05f, -r * .31f, -r * .10f, -r * .24f, -r * .18f, -r * .18f);
            c.drawPath(hair, stroke);

            for (int i = 0; i < 4; i++) {
                float rr = (r * .09f) + i * r * .045f;
                c.drawCircle(-r * .22f, -r * .15f + i * r * .035f, rr, stroke);
            }

            drawStar(c, r * .28f, -r * .04f, r * .075f, s);
        }

        private void drawTailsFace(Canvas c, float r, float s) {
            stroke.setStyle(Paint.Style.STROKE);
            stroke.setStrokeCap(Paint.Cap.ROUND);
            stroke.setStrokeWidth(2.1f * s);
            stroke.setColor(Color.rgb(92, 62, 25));

            Path stem = new Path();
            stem.moveTo(-r * .20f, r * .33f);
            stem.cubicTo(-r * .03f, r * .11f, r * .08f, -r * .10f, r * .21f, -r * .33f);
            c.drawPath(stem, stroke);

            paint.setStyle(Paint.Style.FILL);
            paint.setColor(Color.argb(205, 93, 63, 25));

            for (int i = 0; i < 6; i++) {
                float t = i / 5f;
                float x = -r * .13f + t * r * .30f;
                float y = r * .23f - t * r * .47f;
                drawLeaf(c, x - r * .10f, y, -38f, r * .14f, r * .045f);
                drawLeaf(c, x + r * .10f, y - r * .035f, 42f, r * .14f, r * .045f);
            }

            paint.setColor(Color.rgb(90, 58, 21));
            c.drawCircle(-r * .06f, r * .15f, r * .045f, paint);
            c.drawCircle(r * .08f, r * .05f, r * .042f, paint);
            c.drawCircle(r * .16f, -r * .08f, r * .038f, paint);
        }

        private void drawLeaf(Canvas c, float cx, float cy, float angle, float len, float wid) {
            c.save();
            c.translate(cx, cy);
            c.rotate(angle);
            Path leaf = new Path();
            leaf.moveTo(-len / 2f, 0);
            leaf.quadTo(0, -wid, len / 2f, 0);
            leaf.quadTo(0, wid, -len / 2f, 0);
            leaf.close();
            c.drawPath(leaf, paint);
            c.restore();
        }

        private void drawStar(Canvas c, float cx, float cy, float r, float s) {
            stroke.setStyle(Paint.Style.STROKE);
            stroke.setStrokeWidth(1.25f * s);
            stroke.setColor(Color.rgb(95, 63, 23));
            for (int i = 0; i < 8; i++) {
                double a = i * Math.PI / 4.0;
                float x2 = cx + (float)Math.cos(a) * r;
                float y2 = cy + (float)Math.sin(a) * r;
                c.drawLine(cx, cy, x2, y2, stroke);
            }
        }

        private void drawCoinRimText(Canvas c, String text, float radius, float textSize) {
            paint.setShader(null);
            paint.setStyle(Paint.Style.FILL);
            paint.setTypeface(sansMedium);
            paint.setTextSize(textSize);
            paint.setColor(Color.argb(220, 91, 61, 25));

            String t = text.toUpperCase(Locale.US);
            float start = -132f;
            float sweep = 264f;
            float step = sweep / Math.max(1, t.length() - 1);

            for (int i = 0; i < t.length(); i++) {
                float a = start + i * step;
                double rad = Math.toRadians(a);
                float x = (float)Math.cos(rad) * radius;
                float y = (float)Math.sin(rad) * radius;
                c.save();
                c.translate(x, y);
                c.rotate(a + 90f);
                String ch = String.valueOf(t.charAt(i));
                float tw = paint.measureText(ch);
                c.drawText(ch, -tw / 2f, 0, paint);
                c.restore();
            }
        }

        private void drawResult(Canvas c, int w, int h, boolean dark, float s) {
            int fg = dark ? cream() : ink();
            int muted = dark ? mutedDark() : mutedLight();

            if (flipping) {
                paint.setTypeface(sans);
                paint.setTextSize(8f * s);
                paint.setColor(muted);
                drawSpacedCentered(c, "IT'S IN THE AIR ...", w / 2f, h * .765f, 2.3f * s, paint);
                return;
            }

            if (lastResult == null) {
                paint.setTypeface(sans);
                paint.setTextSize(8f * s);
                paint.setColor(muted);
                drawSpacedCentered(c, "TAP THE COIN TO FLIP", w / 2f, h * .765f, 2.5f * s, paint);
                paint.setTypeface(displayItalic);
                paint.setTextSize(14f * s);
                paint.setColor(muted);
                drawCentered(c, "A small decision. No overthinking.", w / 2f, h * .805f, paint);
            } else {
                paint.setTypeface(sans);
                paint.setTextSize(7.3f * s);
                paint.setColor(muted);
                drawSpacedCentered(c, "THE COIN SAYS", w / 2f, h * .745f, 2.8f * s, paint);

                paint.setTypeface(display);
                paint.setTextSize(43f * s);
                paint.setColor(fg);
                drawCentered(c, lastResult ? "HEADS" : "TAILS", w / 2f, h * .802f, paint);

                paint.setTypeface(displayItalic);
                paint.setTextSize(13f * s);
                paint.setColor(muted);
                drawCentered(
                        c,
                        lastResult ? "Take it as a nudge." : "The other path is still a path.",
                        w / 2f,
                        h * .839f,
                        paint
                );
            }
        }

        private void drawFooter(Canvas c, int w, int h, boolean dark, float s) {
            int muted = dark ? mutedDark() : mutedLight();

            paint.setTypeface(sansMedium);
            paint.setTextSize(7.2f * s);
            paint.setColor(muted);
            String stats = String.format(Locale.US, "%02d TOSSES   ·   %02d HEADS   ·   %02d TAILS", tosses, heads, tails);
            drawSpacedCentered(c, stats, w / 2f, h * .908f, .9f * s, paint);

            paint.setTypeface(sans);
            paint.setTextSize(7.1f * s);
            paint.setColor(Color.argb(dark ? 150 : 135,
                    dark ? 210 : 80,
                    dark ? 201 : 76,
                    dark ? 187 : 69));
            drawSpacedCentered(c, "RESET", w / 2f, h * .956f, 2.2f * s, paint);
        }

        private void drawCentered(Canvas c, String text, float cx, float baseline, Paint p) {
            c.drawText(text, cx - p.measureText(text) / 2f, baseline, p);
        }

        private void drawSpacedCentered(Canvas c, String text, float cx, float baseline, float spacing, Paint p) {
            float width = spacedWidth(text, spacing, p);
            drawSpacedText(c, text, cx - width / 2f, baseline, spacing, p, false);
        }

        private float spacedWidth(String text, float spacing, Paint p) {
            float width = 0f;
            for (int i = 0; i < text.length(); i++) {
                width += p.measureText(String.valueOf(text.charAt(i)));
                if (i < text.length() - 1) width += spacing;
            }
            return width;
        }

        private void drawSpacedText(Canvas c, String text, float x, float baseline, float spacing, Paint p, boolean centered) {
            float cur = x;
            if (centered) cur -= spacedWidth(text, spacing, p) / 2f;
            for (int i = 0; i < text.length(); i++) {
                String ch = String.valueOf(text.charAt(i));
                c.drawText(ch, cur, baseline, p);
                cur += p.measureText(ch) + spacing;
            }
        }

        @Override
        public boolean onTouchEvent(MotionEvent e) {
            if (e.getAction() == MotionEvent.ACTION_DOWN) {
                downX = e.getX();
                downY = e.getY();
                return true;
            }
            if (e.getAction() == MotionEvent.ACTION_UP) {
                float dx = e.getX() - downX;
                float dy = e.getY() - downY;
                if (Math.hypot(dx, dy) < 24f * getResources().getDisplayMetrics().density) {
                    if (e.getY() > getHeight() * .92f) reset();
                    else flip();
                }
                performClick();
                return true;
            }
            return true;
        }

        @Override
        public boolean performClick() {
            super.performClick();
            return true;
        }

        private void flip() {
            if (flipping) return;

            pendingHeads = random.nextBoolean();
            halfTurns = pendingHeads == displayHeads ? 8 : 7;
            flipping = true;
            flipProgress = 0f;

            animator = ValueAnimator.ofFloat(0f, 1f);
            animator.setDuration(1180L);
            animator.setInterpolator(new DecelerateInterpolator());
            animator.addUpdateListener(a -> {
                flipProgress = (float)a.getAnimatedValue();
                invalidate();
            });
            animator.addListener(new AnimatorListenerAdapter() {
                @Override
                public void onAnimationEnd(Animator animation) {
                    displayHeads = pendingHeads;
                    lastResult = pendingHeads;
                    tosses++;
                    if (pendingHeads) heads++; else tails++;
                    flipping = false;
                    flipProgress = 0f;
                    vibrate();
                    invalidate();
                }
            });
            animator.start();
        }

        private void reset() {
            if (flipping) return;
            tosses = 0;
            heads = 0;
            tails = 0;
            lastResult = null;
            displayHeads = true;
            performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP);
            invalidate();
        }

        private void vibrate() {
            performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP);
            try {
                Vibrator v = (Vibrator)getContext().getSystemService(Context.VIBRATOR_SERVICE);
                if (v != null && v.hasVibrator()) {
                    if (android.os.Build.VERSION.SDK_INT >= 26) {
                        v.vibrate(VibrationEffect.createOneShot(28, 90));
                    } else {
                        v.vibrate(28);
                    }
                }
            } catch (Exception ignored) { }
        }
    }
}
