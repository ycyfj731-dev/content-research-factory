package com.wentian.liuyao;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.animation.ValueAnimator;
import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.graphics.*;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.HapticFeedbackConstants;
import android.view.View;
import android.view.animation.DecelerateInterpolator;
import android.view.inputmethod.InputMethodManager;
import android.widget.*;

import java.security.SecureRandom;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class MainActivity extends Activity {

    private static final int BG = Color.rgb(243, 238, 229);
    private static final int INK = Color.rgb(21, 19, 15);
    private static final int MUTED = Color.rgb(105, 98, 87);
    private static final int BRONZE = Color.rgb(145, 94, 47);
    private static final int HAIRLINE = Color.rgb(190, 179, 162);

    private final SecureRandom random = new SecureRandom();
    private LinearLayout root;
    private ScrollView scroll;
    private EditText questionInput;
    private String question = "";

    private final int[] yao = new int[6];
    private final boolean[][] coinSides = new boolean[6][3]; // true=字(3), false=背(2)
    private int currentLine = 0;
    private boolean casting = false;

    private CoinView[] coins;
    private TextView lineTitle;
    private TextView lineResult;
    private TextView castButton;
    private ProgressHexagramView progressView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(BG);
        getWindow().setNavigationBarColor(BG);
        if (android.os.Build.VERSION.SDK_INT >= 26) {
            getWindow().getDecorView().setSystemUiVisibility(
                    View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR
            );
        } else if (android.os.Build.VERSION.SDK_INT >= 23) {
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR);
        }
        showHome();
    }

    private void basePage() {
        scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setOverScrollMode(View.OVER_SCROLL_NEVER);
        scroll.setBackgroundColor(BG);

        root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER_HORIZONTAL);
        root.setPadding(dp(28), dp(24), dp(28), dp(28));
        root.setBackgroundColor(BG);

        scroll.addView(root, new ScrollView.LayoutParams(
                ScrollView.LayoutParams.MATCH_PARENT,
                ScrollView.LayoutParams.WRAP_CONTENT
        ));
        setContentView(scroll);
    }

    private TextView title(String text, float size) {
        TextView t = new TextView(this);
        t.setText(text);
        t.setTextColor(INK);
        t.setTextSize(size);
        t.setGravity(Gravity.CENTER);
        t.setTypeface(Typeface.create("serif", Typeface.NORMAL));
        t.setIncludeFontPadding(false);
        return t;
    }

    private TextView body(String text, float size, int color) {
        TextView t = new TextView(this);
        t.setText(text);
        t.setTextColor(color);
        t.setTextSize(size);
        t.setGravity(Gravity.CENTER);
        t.setTypeface(Typeface.create("sans-serif", Typeface.NORMAL));
        t.setIncludeFontPadding(false);
        return t;
    }

    private TextView button(String text) {
        TextView b = body(text, 15, INK);
        b.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        b.setLetterSpacing(.14f);
        b.setGravity(Gravity.CENTER);

        GradientDrawable gd = new GradientDrawable();
        gd.setColor(Color.TRANSPARENT);
        gd.setStroke(dp(1), INK);
        gd.setCornerRadius(dp(28));
        b.setBackground(gd);
        return b;
    }

    private void showHome() {
        basePage();

        Space top = new Space(this);
        root.addView(top, new LinearLayout.LayoutParams(1, dp(45)));

        TextView logo = title("问天", 58);
        root.addView(logo, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        ));

        Space gap = new Space(this);
        root.addView(gap, new LinearLayout.LayoutParams(1, dp(68)));

        LinearLayout coinRow = new LinearLayout(this);
        coinRow.setOrientation(LinearLayout.HORIZONTAL);
        coinRow.setGravity(Gravity.CENTER);
        for (int i = 0; i < 3; i++) {
            CoinView c = new CoinView(this);
            c.setFace(i != 1);
            LinearLayout.LayoutParams cp = new LinearLayout.LayoutParams(dp(86), dp(86));
            if (i > 0) cp.leftMargin = dp(12);
            coinRow.addView(c, cp);
        }
        root.addView(coinRow);

        Space gap2 = new Space(this);
        root.addView(gap2, new LinearLayout.LayoutParams(1, dp(74)));

        questionInput = new EditText(this);
        questionInput.setSingleLine(false);
        questionInput.setMaxLines(3);
        questionInput.setTextSize(15);
        questionInput.setTextColor(INK);
        questionInput.setHintTextColor(Color.rgb(155, 145, 130));
        questionInput.setHint("所问之事（可不填）");
        questionInput.setGravity(Gravity.CENTER);
        questionInput.setBackgroundColor(Color.TRANSPARENT);
        questionInput.setPadding(dp(10), dp(8), dp(10), dp(8));
        root.addView(questionInput, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(58)
        ));

        View line = new View(this);
        line.setBackgroundColor(HAIRLINE);
        root.addView(line, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(1)
        ));

        TextView start = button("开始起卦");
        LinearLayout.LayoutParams startLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(54)
        );
        startLp.topMargin = dp(34);
        root.addView(start, startLp);
        start.setOnClickListener(v -> beginCasting());

        TextView rule = body("字为 3 · 背为 2", 11, MUTED);
        LinearLayout.LayoutParams ruleLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
        ruleLp.topMargin = dp(22);
        root.addView(rule, ruleLp);
    }

    private void beginCasting() {
        question = questionInput == null ? "" : questionInput.getText().toString().trim();
        hideKeyboard();
        for (int i = 0; i < 6; i++) {
            yao[i] = 0;
            for (int j = 0; j < 3; j++) coinSides[i][j] = false;
        }
        currentLine = 0;
        showCasting();
    }

    private void showCasting() {
        basePage();

        TextView logo = title("问天", 28);
        root.addView(logo, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        ));

        lineTitle = title(lineName(currentLine), 39);
        LinearLayout.LayoutParams lt = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
        lt.topMargin = dp(40);
        root.addView(lineTitle, lt);

        coins = new CoinView[3];
        LinearLayout coinRow = new LinearLayout(this);
        coinRow.setOrientation(LinearLayout.HORIZONTAL);
        coinRow.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams rowLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(122)
        );
        rowLp.topMargin = dp(28);
        root.addView(coinRow, rowLp);

        for (int i = 0; i < 3; i++) {
            coins[i] = new CoinView(this);
            coins[i].setFace(true);
            LinearLayout.LayoutParams cp = new LinearLayout.LayoutParams(dp(96), dp(96));
            if (i > 0) cp.leftMargin = dp(10);
            coinRow.addView(coins[i], cp);
        }

        lineResult = body("三枚铜钱，一次成一爻", 14, MUTED);
        LinearLayout.LayoutParams rr = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
        rr.topMargin = dp(18);
        root.addView(lineResult, rr);

        castButton = button("摇一爻");
        LinearLayout.LayoutParams cb = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(54)
        );
        cb.topMargin = dp(28);
        root.addView(castButton, cb);
        castButton.setOnClickListener(v -> {
            if (currentLine >= 6) showResult();
            else tossCurrentLine();
        });

        progressView = new ProgressHexagramView(this, yao);
        LinearLayout.LayoutParams pv = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(300)
        );
        pv.topMargin = dp(22);
        root.addView(progressView, pv);
    }

    private void tossCurrentLine() {
        if (casting || currentLine >= 6) return;
        casting = true;
        castButton.setAlpha(.45f);
        castButton.setText("铜钱落定…");

        boolean[] target = new boolean[3];
        int sum = 0;
        for (int i = 0; i < 3; i++) {
            target[i] = random.nextBoolean();
            sum += target[i] ? 3 : 2;
        }
        final int finalSum = sum;
        final int lineIndex = currentLine;

        ValueAnimator anim = ValueAnimator.ofFloat(0f, 1f);
        anim.setDuration(1050L);
        anim.setInterpolator(new DecelerateInterpolator());
        anim.addUpdateListener(a -> {
            float p = (float) a.getAnimatedValue();
            for (int i = 0; i < 3; i++) {
                float local = Math.max(0f, Math.min(1f, p * 1.08f - i * .04f));
                float phase = local * (7 + i) * (float)Math.PI;
                float cos = (float)Math.cos(phase);
                coins[i].setScaleX(Math.max(.07f, Math.abs(cos)));
                coins[i].setTranslationY(-dp(34 + i * 5) * 4f * local * (1f-local));
                coins[i].setRotation((float)Math.sin(local * Math.PI) * (i==1 ? -5f : 5f));
                coins[i].setFace(cos >= 0f ? coins[i].isFace() : !coins[i].isFace());
            }
        });
        anim.addListener(new AnimatorListenerAdapter() {
            @Override
            public void onAnimationEnd(Animator animation) {
                for (int i = 0; i < 3; i++) {
                    coinSides[lineIndex][i] = target[i];
                    coins[i].setFace(target[i]);
                    coins[i].setScaleX(1f);
                    coins[i].setTranslationY(0f);
                    coins[i].setRotation(0f);
                }
                yao[lineIndex] = finalSum;
                lineResult.setText(sideText(target) + "    " + finalSum + " · " + yaoType(finalSum));
                progressView.invalidate();
                coins[1].performHapticFeedback(HapticFeedbackConstants.CONFIRM);

                currentLine++;
                casting = false;
                castButton.setAlpha(1f);

                if (currentLine >= 6) {
                    lineTitle.setText("六爻已成");
                    castButton.setText("查看卦象");
                } else {
                    castButton.setText("摇下一爻");
                    lineTitle.setText(lineName(currentLine));
                }
            }
        });
        anim.start();
    }

    private String sideText(boolean[] target) {
        return (target[0] ? "字" : "背") + " · " +
               (target[1] ? "字" : "背") + " · " +
               (target[2] ? "字" : "背");
    }

    private String yaoType(int v) {
        switch (v) {
            case 6: return "老阴";
            case 7: return "少阳";
            case 8: return "少阴";
            case 9: return "老阳";
            default: return "";
        }
    }

    private String lineName(int idx) {
        String[] names = {"初爻","二爻","三爻","四爻","五爻","上爻"};
        if (idx < 0 || idx >= names.length) return "";
        return names[idx];
    }

    private void showResult() {
        if (currentLine < 6) return;
        basePage();

        TextView logo = title("问天", 28);
        root.addView(logo, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        ));

        if (!question.isEmpty()) {
            TextView q = body("“" + question + "”", 14, MUTED);
            q.setTypeface(Typeface.create("serif", Typeface.ITALIC));
            LinearLayout.LayoutParams qlp = new LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
            );
            qlp.topMargin = dp(20);
            root.addView(q, qlp);
        }

        LinearLayout pair = new LinearLayout(this);
        pair.setOrientation(LinearLayout.HORIZONTAL);
        pair.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams pairLp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(295)
        );
        pairLp.topMargin = dp(34);
        root.addView(pair, pairLp);

        pair.addView(hexColumn("本卦", false), new LinearLayout.LayoutParams(0, dp(285), 1f));
        Space centerGap = new Space(this);
        pair.addView(centerGap, new LinearLayout.LayoutParams(dp(18), 1));
        pair.addView(hexColumn("变卦", true), new LinearLayout.LayoutParams(0, dp(285), 1f));

        TextView moving = body(movingText(), 13, MUTED);
        LinearLayout.LayoutParams mlp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
        mlp.topMargin = dp(18);
        root.addView(moving, mlp);

        View hair = new View(this);
        hair.setBackgroundColor(HAIRLINE);
        LinearLayout.LayoutParams hlp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(1)
        );
        hlp.topMargin = dp(28);
        root.addView(hair, hlp);

        TextView recordTitle = body("六次记录", 12, INK);
        recordTitle.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        recordTitle.setLetterSpacing(.16f);
        LinearLayout.LayoutParams rtlp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
        rtlp.topMargin = dp(25);
        root.addView(recordTitle, rtlp);

        for (int i = 5; i >= 0; i--) {
            boolean[] s = coinSides[i];
            String txt = String.format(Locale.CHINA, "%s　%s　%d · %s",
                    lineName(i), sideText(s), yao[i], yaoType(yao[i]));
            TextView row = body(txt, 13, MUTED);
            row.setGravity(Gravity.CENTER);
            LinearLayout.LayoutParams rlp = new LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
            );
            rlp.topMargin = dp(10);
            root.addView(row, rlp);
        }

        TextView copy = button("复制结果");
        LinearLayout.LayoutParams clp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(52)
        );
        clp.topMargin = dp(30);
        root.addView(copy, clp);
        copy.setOnClickListener(v -> copyResult(copy));

        TextView again = body("重新起卦", 13, MUTED);
        again.setGravity(Gravity.CENTER);
        again.setPadding(0, dp(18), 0, dp(18));
        root.addView(again, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        ));
        again.setOnClickListener(v -> showHome());
    }

    private View hexColumn(String label, boolean changed) {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setGravity(Gravity.CENTER_HORIZONTAL);

        TextView lab = body(label, 11, MUTED);
        lab.setLetterSpacing(.18f);
        box.addView(lab, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        ));

        HexagramView hv = new HexagramView(this, yao, changed);
        LinearLayout.LayoutParams hvp = new LinearLayout.LayoutParams(dp(118), dp(178));
        hvp.topMargin = dp(14);
        box.addView(hv, hvp);

        TextView name = title(hexagramName(yao, changed), 25);
        LinearLayout.LayoutParams nlp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
        nlp.topMargin = dp(8);
        box.addView(name, nlp);
        return box;
    }

    private String movingText() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 6; i++) {
            if (yao[i] == 6 || yao[i] == 9) {
                if (sb.length() > 0) sb.append("、");
                sb.append(lineName(i));
            }
        }
        return sb.length() == 0 ? "无动爻" : "动爻：" + sb;
    }

    private String fullResultText() {
        StringBuilder sb = new StringBuilder();
        sb.append("问天\n");
        if (!question.isEmpty()) sb.append("所问：").append(question).append("\n");
        sb.append("本卦：").append(hexagramName(yao, false)).append("\n");
        sb.append("变卦：").append(hexagramName(yao, true)).append("\n");
        sb.append(movingText()).append("\n\n");
        for (int i = 0; i < 6; i++) {
            sb.append(lineName(i)).append("：")
              .append(sideText(coinSides[i])).append(" → ")
              .append(yao[i]).append(" · ").append(yaoType(yao[i])).append("\n");
        }
        sb.append("\n起卦时间：")
          .append(new SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.CHINA).format(new Date()));
        return sb.toString();
    }

    private void copyResult(TextView source) {
        ClipboardManager cm = (ClipboardManager)getSystemService(Context.CLIPBOARD_SERVICE);
        if (cm != null) {
            cm.setPrimaryClip(ClipData.newPlainText("问天起卦结果", fullResultText()));
            source.setText("已复制");
            source.performHapticFeedback(HapticFeedbackConstants.CONFIRM);
        }
    }

    private void hideKeyboard() {
        View v = getCurrentFocus();
        if (v != null) {
            InputMethodManager imm = (InputMethodManager)getSystemService(Context.INPUT_METHOD_SERVICE);
            if (imm != null) imm.hideSoftInputFromWindow(v.getWindowToken(), 0);
            v.clearFocus();
        }
    }

    private int dp(float v) {
        return Math.round(v * getResources().getDisplayMetrics().density);
    }

    private static boolean isYang(int v, boolean changed) {
        boolean yang = (v == 7 || v == 9);
        if (changed && (v == 6 || v == 9)) yang = !yang;
        return yang;
    }

    private static int trigramCode(int[] vals, int offset, boolean changed) {
        int code = 0;
        for (int i = 0; i < 3; i++) {
            if (isYang(vals[offset+i], changed)) code |= (1 << i);
        }
        return code;
    }

    private static String hexagramName(int[] vals, boolean changed) {
        int lower = trigramCode(vals, 0, changed);
        int upper = trigramCode(vals, 3, changed);
        int key = upper * 8 + lower;
        switch (key) {
            case 63: return "乾";
            case 0: return "坤";
            case 17: return "屯";
            case 34: return "蒙";
            case 23: return "需";
            case 58: return "讼";
            case 2: return "师";
            case 16: return "比";
            case 55: return "小畜";
            case 59: return "履";
            case 7: return "泰";
            case 56: return "否";
            case 61: return "同人";
            case 47: return "大有";
            case 4: return "谦";
            case 8: return "豫";
            case 25: return "随";
            case 38: return "蛊";
            case 3: return "临";
            case 48: return "观";
            case 41: return "噬嗑";
            case 37: return "贲";
            case 32: return "剥";
            case 1: return "复";
            case 57: return "无妄";
            case 39: return "大畜";
            case 33: return "颐";
            case 30: return "大过";
            case 18: return "坎";
            case 45: return "离";
            case 28: return "咸";
            case 14: return "恒";
            case 60: return "遁";
            case 15: return "大壮";
            case 40: return "晋";
            case 5: return "明夷";
            case 53: return "家人";
            case 43: return "睽";
            case 20: return "蹇";
            case 10: return "解";
            case 35: return "损";
            case 49: return "益";
            case 31: return "夬";
            case 62: return "姤";
            case 24: return "萃";
            case 6: return "升";
            case 26: return "困";
            case 22: return "井";
            case 29: return "革";
            case 46: return "鼎";
            case 9: return "震";
            case 36: return "艮";
            case 52: return "渐";
            case 11: return "归妹";
            case 13: return "丰";
            case 44: return "旅";
            case 54: return "巽";
            case 27: return "兑";
            case 50: return "涣";
            case 19: return "节";
            case 51: return "中孚";
            case 12: return "小过";
            case 21: return "既济";
            case 42: return "未济";
            default: return "卦";
        }
    }

    private static final class CoinView extends View {
        private final Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
        private final Paint line = new Paint(Paint.ANTI_ALIAS_FLAG);
        private boolean face = true; // true=字 false=背

        CoinView(Context c) {
            super(c);
            setLayerType(View.LAYER_TYPE_SOFTWARE, null);
        }

        boolean isFace() { return face; }
        void setFace(boolean f) { face = f; invalidate(); }

        @Override
        protected void onDraw(Canvas c) {
            super.onDraw(c);
            float w = getWidth(), h = getHeight();
            float cx = w/2f, cy = h/2f;
            float r = Math.min(w,h)*.45f;

            p.setStyle(Paint.Style.FILL);
            p.setShadowLayer(r*.12f, 0, r*.08f, Color.argb(55,0,0,0));
            p.setShader(new RadialGradient(
                    cx-r*.30f, cy-r*.32f, r*1.45f,
                    new int[]{
                            Color.rgb(232,190,126),
                            Color.rgb(185,126,70),
                            Color.rgb(116,72,38),
                            Color.rgb(172,111,58)
                    },
                    new float[]{0f,.38f,.73f,1f},
                    Shader.TileMode.CLAMP
            ));
            c.drawCircle(cx,cy,r,p);
            p.clearShadowLayer();
            p.setShader(null);

            line.setStyle(Paint.Style.STROKE);
            line.setStrokeWidth(Math.max(1.5f,r*.025f));
            line.setColor(Color.rgb(91,56,28));
            c.drawCircle(cx,cy,r-line.getStrokeWidth(),line);

            line.setStrokeWidth(Math.max(1f,r*.010f));
            line.setColor(Color.rgb(239,201,143));
            c.drawCircle(cx,cy,r*.84f,line);

            float hole=r*.20f;
            p.setColor(BG);
            p.setStyle(Paint.Style.FILL);
            c.drawRect(cx-hole,cy-hole,cx+hole,cy+hole,p);
            line.setStyle(Paint.Style.STROKE);
            line.setStrokeWidth(Math.max(1f,r*.018f));
            line.setColor(Color.rgb(86,51,26));
            c.drawRect(cx-hole,cy-hole,cx+hole,cy+hole,line);

            p.setShader(null);
            p.setTextAlign(Paint.Align.CENTER);
            p.setTypeface(Typeface.create("serif",Typeface.BOLD));
            p.setColor(Color.rgb(75,45,23));

            if (face) {
                p.setTextSize(r*.31f);
                c.drawText("問",cx,cy-r*.36f,p);
                c.drawText("天",cx,cy+r*.57f,p);
                p.setTextSize(r*.22f);
                c.drawText("乾",cx-r*.48f,cy+r*.08f,p);
                c.drawText("坤",cx+r*.48f,cy+r*.08f,p);
            } else {
                line.setColor(Color.rgb(79,47,23));
                line.setStrokeWidth(Math.max(1.5f,r*.022f));
                c.drawCircle(cx,cy,r*.60f,line);
                c.drawCircle(cx,cy,r*.50f,line);
                for(int i=0;i<8;i++){
                    double a=i*Math.PI/4d;
                    float x1=cx+(float)Math.cos(a)*r*.30f;
                    float y1=cy+(float)Math.sin(a)*r*.30f;
                    float x2=cx+(float)Math.cos(a)*r*.58f;
                    float y2=cy+(float)Math.sin(a)*r*.58f;
                    c.drawLine(x1,y1,x2,y2,line);
                }
            }
        }
    }

    private static final class ProgressHexagramView extends View {
        private final int[] vals;
        private final Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);

        ProgressHexagramView(Context c, int[] vals) {
            super(c);
            this.vals=vals;
        }

        @Override
        protected void onDraw(Canvas c) {
            super.onDraw(c);
            float w=getWidth(), h=getHeight();
            float center=w*.46f;
            float startY=h*.12f;
            float row=h*.135f;
            String[] names={"上爻","五爻","四爻","三爻","二爻","初爻"};

            for(int visual=0; visual<6; visual++){
                int idx=5-visual;
                float y=startY+visual*row;
                p.setStyle(Paint.Style.FILL);
                p.setTextSize(Math.min(w,h)*.045f);
                p.setTypeface(Typeface.create("sans-serif",Typeface.NORMAL));
                p.setTextAlign(Paint.Align.LEFT);
                p.setColor(vals[idx]==0 ? Color.rgb(177,167,151) : MUTED);
                c.drawText(names[visual],w*.72f,y+5,p);

                if(vals[idx]==0){
                    p.setColor(Color.rgb(205,196,181));
                    c.drawRect(center-w*.19f,y-3,center+w*.19f,y+3,p);
                    continue;
                }
                boolean yang=(vals[idx]==7||vals[idx]==9);
                p.setColor(INK);
                if(yang){
                    c.drawRect(center-w*.19f,y-4,center+w*.19f,y+4,p);
                }else{
                    c.drawRect(center-w*.19f,y-4,center-w*.035f,y+4,p);
                    c.drawRect(center+w*.035f,y-4,center+w*.19f,y+4,p);
                }

                if(vals[idx]==6||vals[idx]==9){
                    p.setStyle(Paint.Style.STROKE);
                    p.setStrokeWidth(2);
                    p.setColor(BRONZE);
                    c.drawCircle(center+w*.255f,y,7,p);
                    p.setStyle(Paint.Style.FILL);
                }
            }
        }
    }

    private static final class HexagramView extends View {
        private final int[] vals;
        private final boolean changed;
        private final Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);

        HexagramView(Context c, int[] vals, boolean changed) {
            super(c);
            this.vals=vals;
            this.changed=changed;
        }

        @Override
        protected void onDraw(Canvas c) {
            super.onDraw(c);
            float w=getWidth(), h=getHeight();
            float center=w/2f;
            float row=h/7.2f;
            float y=row*.80f;

            for(int visual=0;visual<6;visual++){
                int idx=5-visual;
                boolean yang=isYang(vals[idx],changed);
                p.setStyle(Paint.Style.FILL);
                p.setColor(INK);
                float half=w*.39f;
                float gap=w*.075f;
                float thick=Math.max(5f,h*.035f);

                if(yang){
                    c.drawRect(center-half,y-thick/2,center+half,y+thick/2,p);
                }else{
                    c.drawRect(center-half,y-thick/2,center-gap,y+thick/2,p);
                    c.drawRect(center+gap,y-thick/2,center+half,y+thick/2,p);
                }
                y+=row;
            }
        }
    }
}
