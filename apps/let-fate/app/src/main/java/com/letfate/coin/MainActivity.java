package com.letfate.coin;

import android.animation.ValueAnimator;
import android.app.Activity;
import android.graphics.*;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.HapticFeedbackConstants;
import android.view.View;
import android.view.animation.DecelerateInterpolator;
import android.widget.*;

import java.security.SecureRandom;
import java.util.Locale;

public class MainActivity extends Activity {

    private static final int IVORY = Color.rgb(243, 238, 230);
    private static final int INK = Color.rgb(19, 18, 16);
    private static final int BLACK = Color.rgb(12, 12, 11);
    private static final int CREAM = Color.rgb(238, 229, 214);
    private static final int MUTED_LIGHT = Color.rgb(103, 98, 91);
    private static final int MUTED_DARK = Color.rgb(164, 155, 141);

    private final SecureRandom random = new SecureRandom();

    private LinearLayout root;
    private ScrollView scroll;
    private TextView kicker1;
    private TextView kicker2;
    private TextView title;
    private TextView subtitle;
    private TextView section;
    private CoinView coin;
    private TextView resultEyebrow;
    private TextView result;
    private TextView resultNote;
    private TextView flipButton;
    private TextView stats;
    private TextView reset;

    private int tosses = 0;
    private int heads = 0;
    private int tails = 0;
    private boolean currentHeads = true;
    private Boolean lastResult = null;
    private boolean flipping = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        buildUi();
        applyTheme(false);
    }

    private void buildUi() {
        scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setOverScrollMode(View.OVER_SCROLL_NEVER);

        root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER_HORIZONTAL);
        root.setPadding(dp(28), dp(20), dp(28), dp(24));
        scroll.addView(root, new ScrollView.LayoutParams(
                ScrollView.LayoutParams.MATCH_PARENT,
                ScrollView.LayoutParams.WRAP_CONTENT
        ));

        LinearLayout top = new LinearLayout(this);
        top.setOrientation(LinearLayout.HORIZONTAL);
        top.setGravity(Gravity.TOP);
        root.addView(top, lpMatchWrap());

        LinearLayout kickerBox = new LinearLayout(this);
        kickerBox.setOrientation(LinearLayout.VERTICAL);
        LinearLayout.LayoutParams kickerBoxLp = new LinearLayout.LayoutParams(0, dp(55), 1f);
        top.addView(kickerBox, kickerBoxLp);

        kicker1 = smallCaps("A SMALL COIN", 9);
        kicker2 = smallCaps("A BIGGER YOU", 9);
        kickerBox.addView(kicker1);
        kickerBox.addView(kicker2);

        TextView mark = smallCaps("•", 12);
        mark.setGravity(Gravity.END);
        top.addView(mark, new LinearLayout.LayoutParams(dp(30), dp(38)));

        title = new TextView(this);
        title.setText("LET FATE");
        title.setTextSize(54);
        title.setGravity(Gravity.CENTER);
        title.setTypeface(Typeface.create("serif", Typeface.NORMAL));
        title.setIncludeFontPadding(false);
        LinearLayout.LayoutParams titleLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        titleLp.topMargin = dp(6);
        root.addView(title, titleLp);

        subtitle = new TextView(this);
        subtitle.setText("Leave it to chance.");
        subtitle.setTextSize(18);
        subtitle.setGravity(Gravity.CENTER);
        subtitle.setTypeface(Typeface.create("serif", Typeface.ITALIC));
        subtitle.setIncludeFontPadding(false);
        LinearLayout.LayoutParams subLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        subLp.topMargin = dp(5);
        root.addView(subtitle, subLp);

        section = smallCaps("—   C O I N   T O S S   —", 9);
        section.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams sectionLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        sectionLp.topMargin = dp(22);
        root.addView(section, sectionLp);

        coin = new CoinView(this);
        LinearLayout.LayoutParams coinLp = new LinearLayout.LayoutParams(dp(278), dp(278));
        coinLp.topMargin = dp(18);
        root.addView(coin, coinLp);
        coin.setOnClickListener(v -> flip());

        resultEyebrow = smallCaps("TAP THE COIN", 9);
        resultEyebrow.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams eyeLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        eyeLp.topMargin = dp(16);
        root.addView(resultEyebrow, eyeLp);

        result = new TextView(this);
        result.setText("FLIP");
        result.setTextSize(44);
        result.setGravity(Gravity.CENTER);
        result.setTypeface(Typeface.create("serif", Typeface.NORMAL));
        result.setIncludeFontPadding(false);
        LinearLayout.LayoutParams resLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        resLp.topMargin = dp(3);
        root.addView(result, resLp);

        resultNote = new TextView(this);
        resultNote.setText("A small decision. No overthinking.");
        resultNote.setTextSize(14);
        resultNote.setGravity(Gravity.CENTER);
        resultNote.setTypeface(Typeface.create("serif", Typeface.ITALIC));
        resultNote.setIncludeFontPadding(false);
        LinearLayout.LayoutParams noteLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        noteLp.topMargin = dp(5);
        root.addView(resultNote, noteLp);

        flipButton = new TextView(this);
        flipButton.setText("FLIP THE COIN");
        flipButton.setTextSize(13);
        flipButton.setGravity(Gravity.CENTER);
        flipButton.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        flipButton.setLetterSpacing(.16f);
        flipButton.setPadding(dp(10), 0, dp(10), 0);
        flipButton.setOnClickListener(v -> flip());
        LinearLayout.LayoutParams buttonLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(52));
        buttonLp.topMargin = dp(24);
        root.addView(flipButton, buttonLp);

        stats = smallCaps("", 9);
        stats.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams statsLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        statsLp.topMargin = dp(20);
        root.addView(stats, statsLp);

        reset = smallCaps("RESET", 9);
        reset.setGravity(Gravity.CENTER);
        reset.setPadding(dp(8), dp(16), dp(8), dp(16));
        reset.setOnClickListener(v -> resetStats());
        LinearLayout.LayoutParams resetLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        resetLp.topMargin = dp(2);
        root.addView(reset, resetLp);

        updateStats();
        setContentView(scroll);
    }

    private TextView smallCaps(String text, int sp) {
        TextView tv = new TextView(this);
        tv.setText(text);
        tv.setTextSize(sp);
        tv.setTypeface(Typeface.create("sans-serif", Typeface.NORMAL));
        tv.setLetterSpacing(.20f);
        tv.setIncludeFontPadding(false);
        return tv;
    }

    private LinearLayout.LayoutParams lpMatchWrap() {
        return new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
    }

    private void flip() {
        if (flipping) return;

        flipping = true;
        final boolean targetHeads = random.nextBoolean();

        resultEyebrow.setText("FLIP AND SEE");
        result.setText("…");
        resultNote.setText("It's in the air.");
        flipButton.setAlpha(.45f);

        final int halfTurns = (targetHeads == currentHeads) ? 8 : 7;

        ValueAnimator animator = ValueAnimator.ofFloat(0f, 1f);
        animator.setDuration(980L);
        animator.setInterpolator(new DecelerateInterpolator());
        animator.addUpdateListener(a -> {
            float p = (float) a.getAnimatedValue();
            float phase = p * halfTurns * (float) Math.PI;
            float cos = (float) Math.cos(phase);
            coin.setScaleX(Math.max(.07f, Math.abs(cos)));
            coin.setTranslationY(-dp(34) * 4f * p * (1f - p));
            boolean shown = cos >= 0f ? currentHeads : !currentHeads;
            coin.setHeads(shown);
        });
        animator.addListener(new android.animation.AnimatorListenerAdapter() {
            @Override
            public void onAnimationEnd(android.animation.Animator animation) {
                currentHeads = targetHeads;
                coin.setHeads(currentHeads);
                coin.setScaleX(1f);
                coin.setTranslationY(0f);

                lastResult = currentHeads;
                tosses++;
                if (currentHeads) heads++; else tails++;

                resultEyebrow.setText("THE COIN SAYS");
                result.setText(currentHeads ? "HEADS" : "TAILS");
                resultNote.setText(currentHeads
                        ? "Take it as a nudge."
                        : "The other path is still a path.");
                flipButton.setText("FLIP AGAIN");
                flipButton.setAlpha(1f);

                applyTheme(!currentHeads);
                updateStats();
                coin.performHapticFeedback(HapticFeedbackConstants.CONTEXT_CLICK);
                flipping = false;
            }
        });
        animator.start();
    }

    private void resetStats() {
        if (flipping) return;
        tosses = heads = tails = 0;
        lastResult = null;
        currentHeads = true;
        coin.setHeads(true);
        resultEyebrow.setText("TAP THE COIN");
        result.setText("FLIP");
        resultNote.setText("A small decision. No overthinking.");
        flipButton.setText("FLIP THE COIN");
        applyTheme(false);
        updateStats();
        reset.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP);
    }

    private void updateStats() {
        stats.setText(String.format(Locale.US,
                "%02d TOSSES   ·   %02d HEADS   ·   %02d TAILS",
                tosses, heads, tails));
    }

    private void applyTheme(boolean dark) {
        int bg = dark ? BLACK : IVORY;
        int fg = dark ? CREAM : INK;
        int muted = dark ? MUTED_DARK : MUTED_LIGHT;

        root.setBackgroundColor(bg);
        scroll.setBackgroundColor(bg);

        kicker1.setTextColor(muted);
        kicker2.setTextColor(muted);
        title.setTextColor(fg);
        subtitle.setTextColor(muted);
        section.setTextColor(muted);
        resultEyebrow.setTextColor(muted);
        result.setTextColor(fg);
        resultNote.setTextColor(muted);
        stats.setTextColor(muted);
        reset.setTextColor(muted);

        GradientDrawable buttonBg = new GradientDrawable();
        buttonBg.setCornerRadius(dp(28));
        buttonBg.setColor(Color.TRANSPARENT);
        buttonBg.setStroke(dp(1), dark ? Color.rgb(187,177,160) : Color.rgb(46,43,38));
        flipButton.setBackground(buttonBg);
        flipButton.setTextColor(fg);

        getWindow().setStatusBarColor(bg);
        getWindow().setNavigationBarColor(bg);
        if (android.os.Build.VERSION.SDK_INT >= 26) {
            int flags = dark ? 0 :
                    View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR;
            getWindow().getDecorView().setSystemUiVisibility(flags);
        } else if (android.os.Build.VERSION.SDK_INT >= 23) {
            getWindow().getDecorView().setSystemUiVisibility(
                    dark ? 0 : View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
            );
        }
    }

    private int dp(float v) {
        return Math.round(v * getResources().getDisplayMetrics().density);
    }

    private static final class CoinView extends View {
        private final Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
        private final Paint line = new Paint(Paint.ANTI_ALIAS_FLAG);
        private boolean heads = true;

        CoinView(Activity context) {
            super(context);
            setClickable(true);
        }

        void setHeads(boolean value) {
            heads = value;
            invalidate();
        }

        @Override
        protected void onDraw(Canvas c) {
            super.onDraw(c);
            float w = getWidth();
            float h = getHeight();
            float cx = w / 2f;
            float cy = h / 2f;
            float r = Math.min(w, h) * .46f;

            p.setStyle(Paint.Style.FILL);
            p.setShader(new RadialGradient(
                    cx - r * .28f, cy - r * .32f, r * 1.45f,
                    new int[]{
                            Color.rgb(253, 237, 190),
                            Color.rgb(224, 190, 118),
                            Color.rgb(166, 123, 55),
                            Color.rgb(232, 198, 126)
                    },
                    new float[]{0f, .42f, .72f, 1f},
                    Shader.TileMode.CLAMP
            ));
            c.drawCircle(cx, cy, r, p);
            p.setShader(null);

            line.setStyle(Paint.Style.STROKE);
            line.setStrokeWidth(Math.max(2f, r * .027f));
            line.setColor(Color.rgb(112, 78, 31));
            c.drawCircle(cx, cy, r - line.getStrokeWidth(), line);

            line.setStrokeWidth(Math.max(1f, r * .010f));
            line.setColor(Color.rgb(252, 231, 174));
            c.drawCircle(cx, cy, r * .91f, line);

            line.setPathEffect(new DashPathEffect(
                    new float[]{Math.max(2f, r * .018f), Math.max(3f, r * .026f)}, 0));
            line.setStrokeWidth(Math.max(1f, r * .012f));
            line.setColor(Color.rgb(120, 84, 35));
            c.drawCircle(cx, cy, r * .72f, line);
            line.setPathEffect(null);

            p.setColor(Color.rgb(87, 58, 23));
            p.setStyle(Paint.Style.FILL);

            if (heads) drawProfile(c, cx, cy, r);
            else drawBranch(c, cx, cy, r);

            p.setTypeface(Typeface.create("serif", Typeface.NORMAL));
            p.setTextAlign(Paint.Align.CENTER);
            p.setTextSize(r * .105f);
            p.setColor(Color.rgb(96, 65, 25));
            c.drawText(heads ? "LET FATE" : "TAKE TIME", cx, cy - r * .63f, p);

            p.setTextSize(r * .08f);
            p.setLetterSpacing(0);
            c.drawText(heads ? "MMXXVI" : "GOOD THINGS", cx, cy + r * .67f, p);
        }

        private void drawProfile(Canvas c, float cx, float cy, float r) {
            Path face = new Path();
            face.moveTo(cx - r * .23f, cy + r * .34f);
            face.cubicTo(cx - r * .31f, cy + r * .11f,
                    cx - r * .29f, cy - r * .08f,
                    cx - r * .17f, cy - r * .27f);
            face.cubicTo(cx - r * .08f, cy - r * .42f,
                    cx + r * .04f, cy - r * .43f,
                    cx + r * .11f, cy - r * .31f);
            face.cubicTo(cx + r * .14f, cy - r * .25f,
                    cx + r * .11f, cy - r * .21f,
                    cx + r * .18f, cy - r * .18f);
            face.lineTo(cx + r * .28f, cy - r * .13f);
            face.lineTo(cx + r * .18f, cy - r * .07f);
            face.cubicTo(cx + r * .13f, cy - r * .01f,
                    cx + r * .12f, cy + r * .08f,
                    cx + r * .08f, cy + r * .15f);
            face.cubicTo(cx + r * .03f, cy + r * .23f,
                    cx - r * .02f, cy + r * .27f,
                    cx - r * .07f, cy + r * .28f);
            face.lineTo(cx - r * .01f, cy + r * .40f);
            face.close();
            c.drawPath(face, p);

            line.setStyle(Paint.Style.STROKE);
            line.setStrokeWidth(Math.max(1.5f, r * .012f));
            line.setColor(Color.rgb(235, 200, 128));

            Path hair = new Path();
            hair.moveTo(cx - r * .24f, cy + r * .05f);
            hair.cubicTo(cx - r * .42f, cy - r * .08f,
                    cx - r * .37f, cy - r * .35f,
                    cx - r * .11f, cy - r * .41f);
            hair.cubicTo(cx - r * .03f, cy - r * .31f,
                    cx - r * .09f, cy - r * .22f,
                    cx - r * .19f, cy - r * .17f);
            c.drawPath(hair, line);

            for (int i=0; i<4; i++) {
                float rr = r * (.075f + i * .035f);
                c.drawCircle(cx - r * .22f, cy - r * .15f + i * r * .035f, rr, line);
            }

            float sx = cx + r * .29f;
            float sy = cy - r * .03f;
            for (int i=0; i<8; i++) {
                double a = i * Math.PI / 4d;
                c.drawLine(sx, sy,
                        sx + (float)Math.cos(a) * r * .07f,
                        sy + (float)Math.sin(a) * r * .07f,
                        line);
            }
        }

        private void drawBranch(Canvas c, float cx, float cy, float r) {
            line.setStyle(Paint.Style.STROKE);
            line.setStrokeCap(Paint.Cap.ROUND);
            line.setStrokeWidth(Math.max(2f, r * .018f));
            line.setColor(Color.rgb(88, 58, 22));

            Path stem = new Path();
            stem.moveTo(cx - r * .21f, cy + r * .34f);
            stem.cubicTo(cx - r * .05f, cy + r * .12f,
                    cx + r * .08f, cy - r * .12f,
                    cx + r * .21f, cy - r * .35f);
            c.drawPath(stem, line);

            p.setColor(Color.rgb(88, 58, 22));
            for (int i=0; i<6; i++) {
                float t = i / 5f;
                float x = cx - r * .12f + t * r * .29f;
                float y = cy + r * .22f - t * r * .47f;
                drawLeaf(c, x-r*.10f, y, -38f, r*.15f, r*.046f);
                drawLeaf(c, x+r*.10f, y-r*.04f, 42f, r*.15f, r*.046f);
            }

            c.drawCircle(cx-r*.05f, cy+r*.15f, r*.045f, p);
            c.drawCircle(cx+r*.08f, cy+r*.05f, r*.042f, p);
            c.drawCircle(cx+r*.16f, cy-r*.08f, r*.038f, p);
        }

        private void drawLeaf(Canvas c, float cx, float cy, float angle, float len, float wid) {
            c.save();
            c.translate(cx, cy);
            c.rotate(angle);
            Path leaf = new Path();
            leaf.moveTo(-len/2f, 0);
            leaf.quadTo(0, -wid, len/2f, 0);
            leaf.quadTo(0, wid, -len/2f, 0);
            leaf.close();
            c.drawPath(leaf, p);
            c.restore();
        }
    }
}
