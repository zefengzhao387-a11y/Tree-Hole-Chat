<template>
  <div class="landing" :class="{ entering: isEntering }">
    <!-- 木质底纹 + 风吹粒子 -->
    <div class="ambient" aria-hidden="true">
      <div class="breeze-wave breeze-1" />
      <div class="breeze-wave breeze-2" />
      <div class="breeze-wave breeze-3" />
    </div>

    <header class="hero">
      <div class="brand-row">
        <img src="/logo.png" alt="" class="brand-logo" aria-hidden="true" />
        <div class="brand-text">
          <BlurText
            tag="h1"
            class="brand-title"
            text="解忧树洞"
            animate-by="chars"
            :delay="100"
          />
          <ShinyText tag="p" class="brand-tagline" text="心事有所寄，烦忧有人听" :speed="4" />
          <span class="brand-accent" aria-hidden="true" />
        </div>
      </div>
    </header>

    <section class="tree-stage" aria-label="功能导览">
      <svg class="branches" viewBox="0 0 1000 620" preserveAspectRatio="xMidYMid meet">
        <path
          v-for="(f, i) in features"
          :key="'line-' + i"
          :d="branchPath(f.anchor)"
          class="branch-line"
          :style="{ animationDelay: `${i * 0.6}s` }"
        />
      </svg>

      <article
        v-for="(f, i) in features"
        :key="f.title"
        class="feature-node"
        :class="[
          f.side,
          'node-' + i,
          { dimmed: !!activeFeature },
        ]"
        :style="nodeStyle(f.anchor)"
      >
        <button
          type="button"
          class="feature-card-btn"
          :aria-label="`了解${f.title}`"
          :disabled="!!activeFeature"
          @click="onFeatureClick(i, $event)"
        >
          <div class="feature-card">
            <h3>{{ f.title }}</h3>
            <p>{{ f.desc }}</p>
            <span class="tap-hint">点击了解更多</span>
          </div>
        </button>
      </article>

      <div class="tree-core">
        <!-- 树下层落叶 -->
        <div class="canopy-leaves leaves-below" aria-hidden="true">
          <span
            v-for="n in 4"
            :key="'fall-b-' + n"
            class="fall-leaf"
            :class="'fall-' + (n % 3)"
            :style="fallLeafStyle(n, 'below')"
          />
        </div>

        <img
          v-if="showTreeImage"
          :src="treeHeroSrc"
          alt="解忧树洞"
          class="tree-art"
          @error="onTreeImageError"
        />
        <svg v-else class="tree-placeholder" viewBox="0 0 400 520" fill="none">
          <rect x="172" y="280" width="56" height="160" rx="8" fill="#8b7355" />
          <ellipse cx="200" cy="220" rx="140" ry="120" fill="#6a9470" opacity="0.85" />
        </svg>

        <!-- 树上层落叶 -->
        <div class="canopy-leaves leaves-above" aria-hidden="true">
          <span
            v-for="n in 4"
            :key="'fall-a-' + n"
            class="fall-leaf"
            :class="'fall-' + ((n + 1) % 3)"
            :style="fallLeafStyle(n + 4, 'above')"
          />
        </div>

        <!-- 树洞入口：光晕 + 可点击热区 + 箭头引导 -->
        <div class="hole-entry" :class="{ entering: isEntering }">
          <button
            class="hole-hotspot"
            type="button"
            aria-label="进入树洞"
            @click="enterTreeHole"
          />

          <div class="hole-cue">
            <svg class="cue-arrow" viewBox="0 0 64 32" fill="none" aria-hidden="true">
              <path
                class="cue-path"
                d="M58 16 C46 16, 36 14, 26 12 C20 10, 14 8, 8 6"
                stroke="currentColor"
                stroke-width="2.5"
                stroke-linecap="round"
              />
              <path
                class="cue-head"
                d="M8 6 L14 2 M8 6 L14 10"
                stroke="currentColor"
                stroke-width="2.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
            <span class="cue-text">进入树洞</span>
          </div>
        </div>
      </div>
    </section>

    <footer class="footer">
      <FadeContent direction="up" :delay="200">
        <p>每一份心情，都值得被温柔以待</p>
      </FadeContent>
    </footer>

    <FeatureDetailModal
      v-if="activeFeature"
      :feature="activeFeature"
      :origin="expandOrigin"
      @close="closeDetail"
      @go="goFeature"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import BlurText from '../components/animate/BlurText.vue'
import ShinyText from '../components/animate/ShinyText.vue'
import FadeContent from '../components/animate/FadeContent.vue'
import FeatureDetailModal from '../components/landing/FeatureDetailModal.vue'

const router = useRouter()
const auth = useAuthStore()

const treeHeroSrc = `${import.meta.env.BASE_URL}landing/tree-hero.png`
const showTreeImage = ref(true)
const isEntering = ref(false)

const activeFeature = ref(null)
const expandOrigin = ref(null)

function onTreeImageError() {
  showTreeImage.value = false
}

const features = [
  {
    title: '写日记',
    side: 'left',
    icon: '✍️',
    desc: '随时写下生活片段与心底感受，把每一刻真实情绪留在这里',
    detailTitle: '把心事安放在纸页之间',
    detailIntro: '日记是本系统一切智能体验的起点。你可以自由记录标题、正文与心情标签，系统会安全保存并在后台完成情感分析与向量索引，为后续树洞对话提供「记得你」的私人记忆。',
    highlights: [
      '支持新建、编辑、删除与分页浏览，按心情筛选历史记录',
      '保存后自动调用 DeepSeek 进行结构化情感分析',
      '日记内容自动分块向量化，写入 Chroma 私有知识库',
    ],
    tech: ['SQLite', 'LLM 情感分析', 'RAG 索引'],
    route: '/diary/new',
    cta: '开始写日记',
    anchor: { x: 17, y: 26 },
  },
  {
    title: 'AI 读心',
    side: 'left',
    icon: '🌿',
    desc: '智能读懂日记文字，分析你话语背后的情感与心绪变化',
    detailTitle: '读懂文字背后的情绪',
    detailIntro: '基于大语言模型的情感分析模块，会从你的日记中识别主情绪、情感极性、强度、关键词与温暖建议，帮助你看清自己当下的内心状态。',
    highlights: [
      '输出主情绪、八维情感得分、积极/消极/中性极性',
      '生成一句话摘要与基于状态的短建议',
      '结果持久化存储，可在趋势页汇总展示',
    ],
    tech: ['DeepSeek', 'Prompt Engineering', 'JSON 结构化输出'],
    route: '/diary',
    cta: '查看我的日记',
    anchor: { x: 15, y: 54 },
  },
  {
    title: '解忧树洞',
    side: 'right',
    icon: '🌳',
    desc: '向小树洞倾诉烦恼与秘密，获得温柔回应与安静陪伴',
    detailTitle: '会记得你的树洞伙伴',
    detailIntro: '「小树」不是空泛的聊天机器人。系统会从你的历史日记中检索相关片段，结合对话记忆生成共情式回复，并在合适时自然引用你曾写下的故事。',
    highlights: [
      'RAG 混合检索：向量语义 + BM25 关键词，按用户隔离',
      'SSE 流式输出，打字机式实时回复',
      '标注关联日记编号，回复有据可查',
    ],
    tech: ['LangChain RAG', 'Chroma', 'SSE 流式'],
    route: '/chat',
    cta: '进入树洞对话',
    anchor: { x: 83, y: 28 },
  },
  {
    title: '心情轨迹',
    side: 'right',
    icon: '📈',
    desc: '串联日记里的情绪起伏，看见自己心情如何流动与生长',
    detailTitle: '看见情绪的流动',
    detailIntro: '按日期范围统计你的日记情感数据，以折线图展示情绪强度变化，并由 LLM 生成区间情感总结与温柔建议，帮助你在更长的时间尺度上理解自己。',
    highlights: [
      'ECharts 可视化情绪强度曲线',
      '积极 / 消极 / 中性分布统计',
      'LLM 生成区间情感报告与建议',
    ],
    tech: ['ECharts', '情感趋势 API', 'LLM 报告'],
    route: '/trend',
    cta: '查看心情轨迹',
    anchor: { x: 85, y: 56 },
  },
]

const TRUNK = { x: 50, y: 62 }

function nodeStyle(anchor) {
  return { left: anchor.x + '%', top: anchor.y + '%' }
}

function branchPath(anchor) {
  const sx = TRUNK.x * 10
  const sy = TRUNK.y * 6.2
  const ex = anchor.x * 10
  const ey = anchor.y * 6.2
  const cx1 = sx + (ex - sx) * 0.35
  const cy1 = sy - 40
  const cx2 = ex - (ex - sx) * 0.2
  const cy2 = ey - 20
  return `M ${sx} ${sy} C ${cx1} ${cy1}, ${cx2} ${cy2}, ${ex} ${ey}`
}

function fallLeafStyle(n, layer = 'above') {
  const isBelow = layer === 'below'
  const left = isBelow
    ? 20 + ((n * 23 + 11) % 54)
    : 32 + ((n * 17 + 6) % 36)
  const top = isBelow
    ? 14 + ((n * 11 + 4) % 20)
    : 10 + ((n * 13 + 2) % 18)
  const delay = (n * 2.4) % 16
  const dur = 12 + (n % 4) * 3.5
  const size = (isBelow ? 14 : 16) + (n % 3) * 2
  const drift = (n % 2 === 0 ? 1 : -1) * (10 + (n % 4) * 6)
  const tilt = (n % 2 === 0 ? 1 : -1) * (6 + n * 3)
  return {
    left: left + '%',
    top: top + '%',
    width: size + 'px',
    height: Math.round(size * 0.68) + 'px',
    animationDelay: delay + 's',
    animationDuration: dur + 's',
    '--drift': drift + 'px',
    '--tilt': tilt + 'deg',
  }
}

function enterTreeHole() {
  if (isEntering.value || activeFeature.value) return
  isEntering.value = true
  window.setTimeout(() => {
    router.push(auth.isLoggedIn ? '/diary' : '/auth')
  }, 880)
}

function onFeatureClick(index, event) {
  if (activeFeature.value) return
  const rect = event.currentTarget.getBoundingClientRect()
  expandOrigin.value = {
    top: rect.top,
    left: rect.left,
    width: rect.width,
    height: rect.height,
  }
  activeFeature.value = features[index]
}

function closeDetail() {
  activeFeature.value = null
  expandOrigin.value = null
}

function goFeature(route) {
  closeDetail()
  if (!auth.isLoggedIn && route !== '/') {
    router.push('/auth')
    return
  }
  router.push(route)
}

</script>

<style scoped>
/* ── 木质纸感底 + 风吹氛围 ── */
.landing {
  --wood: #8b7355;
  --wood-deep: #5c4a38;
  --wood-light: #f5ebe0;
  --hole-origin-x: 50%;
  --hole-origin-y: 58%;

  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
  background-color: #f4ede4;
  background-image:
    radial-gradient(ellipse 120% 80% at 50% -10%, rgba(90, 122, 98, 0.07), transparent 50%),
    repeating-linear-gradient(
      92deg,
      transparent 0,
      transparent 3px,
      rgba(139, 115, 85, 0.028) 3px,
      rgba(139, 115, 85, 0.028) 4px
    ),
    repeating-linear-gradient(
      0deg,
      transparent 0,
      transparent 11px,
      rgba(160, 130, 95, 0.018) 11px,
      rgba(160, 130, 95, 0.018) 12px
    ),
    linear-gradient(180deg, #f7f2ea 0%, #f0e8dc 100%);
}

.ambient {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

/* 背景微风层：缓慢漂移的光晕 */
.breeze-wave {
  position: absolute;
  width: 62%;
  height: 42%;
  border-radius: 50%;
  background: radial-gradient(ellipse, rgba(90, 122, 98, 0.14) 0%, rgba(90, 122, 98, 0.04) 45%, transparent 72%);
  animation: breeze-drift ease-in-out infinite;
}

.breeze-1 { top: 6%; left: -6%; animation-duration: 11s; }
.breeze-2 { top: 40%; left: 34%; animation-duration: 14s; animation-delay: 2.5s; opacity: 0.9; }
.breeze-3 { top: 66%; left: 8%; animation-duration: 12s; animation-delay: 5s; opacity: 0.75; }

@keyframes breeze-drift {
  0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.55; }
  50% { transform: translate(52px, -20px) scale(1.1); opacity: 0.95; }
}

/* 从大树树冠飘落的叶子 · 分层 */
.canopy-leaves {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: visible;
}

.leaves-below {
  z-index: 0;
}

.leaves-above {
  z-index: 2;
}

.leaves-below .fall-leaf {
  filter: saturate(0.88) brightness(0.96);
}

.leaves-above .fall-leaf {
  filter: saturate(0.92) brightness(1.02);
}

.fall-leaf {
  position: absolute;
  opacity: 0;
  pointer-events: none;
  animation: leaf-fall ease-in-out infinite;
  transform-origin: center top;
}

.fall-leaf::before {
  content: '';
  position: absolute;
  left: 42%;
  top: 8%;
  width: 1px;
  height: 72%;
  background: linear-gradient(180deg, rgba(58, 52, 46, 0.18), transparent);
  transform: rotate(var(--tilt, -6deg));
  border-radius: 1px;
}

.fall-leaf.fall-0 {
  border-radius: 3px 22px 4px 20px;
  background: linear-gradient(
    155deg,
    rgba(138, 168, 118, 0.92) 0%,
    rgba(106, 138, 96, 0.88) 45%,
    rgba(168, 148, 108, 0.72) 100%
  );
  box-shadow: 0 2px 10px rgba(58, 52, 46, 0.06);
}

.fall-leaf.fall-1 {
  border-radius: 22px 4px 20px 3px;
  background: linear-gradient(
    145deg,
    rgba(184, 152, 104, 0.9) 0%,
    rgba(154, 122, 82, 0.85) 50%,
    rgba(122, 148, 108, 0.7) 100%
  );
  box-shadow: 0 2px 10px rgba(58, 52, 46, 0.06);
}

.fall-leaf.fall-2 {
  border-radius: 18px 18px 6px 6px;
  background: linear-gradient(
    160deg,
    rgba(122, 158, 112, 0.9) 0%,
    rgba(96, 128, 92, 0.86) 55%,
    rgba(140, 168, 124, 0.75) 100%
  );
  box-shadow: 0 2px 10px rgba(58, 52, 46, 0.06);
}

@keyframes leaf-fall {
  0% {
    transform: translate(0, 0) rotate(0deg) scale(0.92);
    opacity: 0;
  }
  8% { opacity: 0.78; }
  30% { transform: translate(calc(var(--drift, 12px) * 0.45), 22vh) rotate(28deg) scale(1); }
  55% { transform: translate(calc(var(--drift, 12px) * -0.25), 44vh) rotate(72deg) scale(0.98); }
  78% { transform: translate(calc(var(--drift, 12px) * 0.7), 64vh) rotate(118deg) scale(0.96); opacity: 0.5; }
  100% {
    transform: translate(var(--drift, 12px), 78vh) rotate(165deg) scale(0.9);
    opacity: 0;
  }
}

.hero {
  position: absolute;
  top: 48px;
  left: 56px;
  z-index: 10;
}

.brand-row {
  display: flex;
  align-items: center;
  gap: clamp(12px, 1.8vw, 18px);
}

.brand-logo {
  width: clamp(52px, 6.5vw, 68px);
  height: clamp(52px, 6.5vw, 68px);
  object-fit: contain;
  flex-shrink: 0;
  align-self: flex-start;
  margin-top: 2px;
  animation: brand-logo-in 0.7s cubic-bezier(0.34, 1.2, 0.64, 1) backwards;
}

.brand-text {
  min-width: 0;
}

@keyframes brand-logo-in {
  from {
    opacity: 0;
    transform: scale(0.92);
  }
}

.brand-title {
  display: block;
  font-family: var(--font-handwrite);
  font-size: clamp(2.125rem, 5.5vw, 2.875rem);
  font-weight: 400;
  line-height: 1.1;
  letter-spacing: 0.02em;
}

.brand-title :deep(.blur-text-segment) {
  color: var(--c-wood-deep);
  text-shadow: var(--grass-shadow);
}

.brand-tagline {
  display: block;
  margin-top: 12px;
  padding-left: 2px;
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  letter-spacing: 0.22em;
}

.brand-accent {
  position: relative;
  display: block;
  width: 56px;
  height: 2px;
  margin-top: 14px;
  margin-left: 2px;
  border-radius: 2px;
  background: linear-gradient(90deg, rgba(92, 74, 56, 0.55), rgba(90, 122, 98, 0.35), transparent);
  animation: brand-accent-in 0.6s ease 0.65s backwards;
}

.brand-accent::after {
  content: '';
  position: absolute;
  left: 52px;
  top: -3px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(90, 122, 98, 0.35);
}

@keyframes brand-char-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
}

@keyframes brand-char-sway {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-2px); }
}

@keyframes brand-tagline-in {
  from { opacity: 0; transform: translateY(6px); }
}

@keyframes brand-accent-in {
  from { opacity: 0; transform: scaleX(0.3); }
}

/* ── 大树舞台 ── */
.tree-stage {
  position: relative;
  z-index: 1;
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.branches {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.branch-line {
  fill: none;
  stroke: #b8c9b0;
  stroke-width: 1.5;
  stroke-linecap: round;
  opacity: 0.22;
  animation: branch-breathe 5s ease-in-out infinite;
}

@keyframes branch-breathe {
  0%, 100% { opacity: 0.18; }
  50% { opacity: 0.28; }
}

.tree-core {
  --hole-x: 50%;
  --hole-y: 58%;
  position: relative;
  width: min(142vw, 1920px);
  z-index: 2;
  flex-shrink: 0;
  transform-origin: 50% 92%;
  animation: tree-sway 9s ease-in-out infinite;
  overflow: visible;
}

@keyframes tree-sway {
  0%, 100% { transform: rotate(-0.35deg); }
  50% { transform: rotate(0.45deg); }
}

.tree-art,
.tree-placeholder {
  position: relative;
  z-index: 1;
  width: 100%;
  height: auto;
  display: block;
  max-height: 100vh;
  object-fit: contain;
  filter: drop-shadow(0 20px 48px rgba(90, 70, 50, 0.1));
}

/* ── 树洞入口 · 箭头引导 ── */
.hole-entry {
  --hole-x: 50%;
  --hole-y: 58%;
  position: absolute;
  left: var(--hole-x);
  top: var(--hole-y);
  transform: translate(-50%, -50%);
  z-index: 20;
  width: 0;
  height: 0;
  overflow: visible;
}

.hole-hotspot {
  position: absolute;
  left: 50%;
  top: 50%;
  width: clamp(64px, 7.5vw, 100px);
  height: clamp(64px, 7.5vw, 100px);
  transform: translate(-50%, -50%);
  border: none;
  border-radius: 50%;
  background: transparent;
  cursor: pointer;
  z-index: 3;
  transition: transform 0.38s cubic-bezier(0.34, 1.2, 0.64, 1);
}

.hole-entry:hover .hole-hotspot,
.hole-entry:focus-within .hole-hotspot {
  transform: translate(-50%, -50%) scale(1.1);
}

.hole-entry:hover .hole-cue,
.hole-entry:focus-within .hole-cue {
  animation: none;
  transform: translateY(-50%) translateX(-6px);
}

.hole-entry:hover .cue-text,
.hole-entry:focus-within .cue-text {
  color: var(--wood-deep);
  letter-spacing: 0.2em;
}

.hole-entry:hover .cue-arrow,
.hole-entry:focus-within .cue-arrow {
  transform: translateX(-10px) scale(1.1);
  color: var(--wood-deep);
}

.cue-text {
  font-family: var(--font-handwrite);
  font-size: clamp(1.125rem, 2.2vw, 1.3125rem);
  font-weight: 400;
  color: #3a342e;
  letter-spacing: 0.04em;
  white-space: nowrap;
  text-shadow: var(--grass-shadow);
  transition:
    color 0.35s ease,
    letter-spacing 0.38s cubic-bezier(0.34, 1.2, 0.64, 1);
}

.cue-arrow {
  width: clamp(32px, 4vw, 48px);
  height: auto;
  flex-shrink: 0;
  color: #8b7355;
  transition: transform 0.38s cubic-bezier(0.34, 1.2, 0.64, 1), color 0.35s ease;
}

.hole-cue {
  position: absolute;
  left: clamp(46px, 5.5vw, 72px);
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  pointer-events: none;
  z-index: 4;
  animation: cue-float-h 4s ease-in-out infinite;
  transition: transform 0.38s cubic-bezier(0.34, 1.2, 0.64, 1);
}

@keyframes cue-float-h {
  0%, 100% { transform: translateY(-50%) translateX(0); }
  50% { transform: translateY(-50%) translateX(4px); }
}

/* 点击进入：由远及近放大树洞 */
.landing.entering {
  overflow: hidden;
  animation: hole-zoom-in 0.88s cubic-bezier(0.22, 0.61, 0.36, 1) forwards;
  transform-origin: var(--hole-origin-x) var(--hole-origin-y);
  will-change: transform, opacity;
}

@keyframes hole-zoom-in {
  0% {
    transform: scale(1);
    opacity: 1;
    filter: blur(0);
  }
  70% {
    opacity: 1;
    filter: blur(0);
  }
  100% {
    transform: scale(4.2);
    opacity: 0;
    filter: blur(0.6px);
  }
}

.hole-entry.entering .hole-cue {
  animation: none;
  opacity: 0;
  transform: translateY(-50%) translateX(12px);
  transition: opacity 0.25s ease, transform 0.25s ease;
}

/* ── 功能卡片 ── */
@keyframes card-sway {
  0%, 100% { transform: translate(calc(-50% + 6px), -50%) translateY(0); }
  50% { transform: translate(calc(-50% + 6px), -50%) translateY(-6px); }
}

@keyframes card-sway-left {
  0%, 100% { transform: translate(calc(-50% - 6px), -50%) translateY(0); }
  50% { transform: translate(calc(-50% - 6px), -50%) translateY(-6px); }
}

.feature-node {
  position: absolute;
  z-index: 4;
  width: max-content;
  max-width: 236px;
  animation: card-sway 7s ease-in-out infinite;
  transition: opacity 0.35s ease, filter 0.35s ease;
}

.feature-node.dimmed {
  opacity: 0.35;
  filter: blur(1px);
  pointer-events: none;
}

.feature-node.left {
  animation-name: card-sway-left;
}

.feature-node.right {
  animation-name: card-sway;
}

.feature-node.node-0 { animation-delay: 0s; }
.feature-node.node-1 { animation-delay: 1.2s; }
.feature-node.node-2 { animation-delay: 0.6s; }
.feature-node.node-3 { animation-delay: 1.8s; }

.feature-card-btn {
  display: block;
  width: 100%;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
  text-align: inherit;
  -webkit-tap-highlight-color: transparent;
}

.feature-card-btn:disabled {
  cursor: default;
}

.feature-card {
  width: 100%;
  min-width: 196px;
  max-width: 236px;
  padding: 14px 18px 12px;
  border-radius: 14px;
  overflow: hidden;
  background: rgba(255, 252, 248, 0.88);
  border: 1px solid rgba(255, 255, 255, 0.65);
  box-shadow:
    0 4px 20px rgba(58, 52, 46, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(10px);
  transition: transform 0.28s ease, box-shadow 0.28s ease;
}

.feature-node.left .feature-card {
  text-align: right;
}

.feature-node.right .feature-card {
  text-align: center;
}

.feature-card-btn:hover:not(:disabled) .feature-card {
  transform: translateY(-3px);
  box-shadow:
    0 10px 28px rgba(58, 52, 46, 0.12),
    0 0 20px rgba(90, 122, 98, 0.08);
}

.feature-node h3 {
  font-family: var(--font-handwrite);
  font-size: 1.375rem;
  font-weight: 400;
  color: #3a342e;
  margin-bottom: 5px;
  letter-spacing: 0.02em;
  line-height: 1.25;
  text-shadow: var(--grass-shadow);
}

.feature-node p {
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: #6a6258;
  line-height: 1.5;
  opacity: 0.92;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-word;
}

.tap-hint {
  display: block;
  margin-top: 8px;
  font-family: var(--font-ui);
  font-size: 0.625rem;
  letter-spacing: 0.06em;
  color: var(--c-primary);
  opacity: 0.8;
}

.feature-node.left .tap-hint {
  text-align: right;
}

.footer {
  position: absolute;
  bottom: 18px;
  left: 0;
  right: 0;
  text-align: center;
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: #a89888;
  z-index: 5;
  pointer-events: none;
}

.footer p:first-child {
  font-style: italic;
  letter-spacing: 0.06em;
}

@media (prefers-reduced-motion: reduce) {
  .tree-core,
  .feature-node,
  .branch-line,
  .fall-leaf,
  .breeze-wave,
  .hole-cue,
  .brand-logo,
  .brand-accent {
    animation: none !important;
  }

  .landing.entering {
    animation: none;
    opacity: 0;
    transition: opacity 0.2s ease;
  }
}

@media (max-width: 768px) {
  .hero { top: 36px; left: 40px; }

  .brand-logo {
    width: 44px;
    height: 44px;
    margin-top: 1px;
  }

  .brand-row { gap: 10px; }

  .brand-title { font-size: clamp(1.75rem, 8vw, 2.25rem); }

  .brand-tagline {
    font-size: 0.75rem;
    letter-spacing: 0.16em;
  }

  .feature-node {
    max-width: 200px;
  }

  .feature-card {
    min-width: 172px;
    max-width: 200px;
    padding: 12px 14px 10px;
  }

  .feature-node h3 { font-size: 1.25rem; }

  .feature-node p { font-size: 0.75rem; line-height: 1.45; -webkit-line-clamp: 2; }

  .tap-hint { font-size: 0.5625rem; margin-top: 6px; }

  .node-0 { left: 8% !important; top: 20% !important; }
  .node-1 { left: 6% !important; top: 48% !important; }
  .node-2 { left: 92% !important; top: 22% !important; }
  .node-3 { left: 94% !important; top: 50% !important; }

  .tree-core { width: 138vw; }

  .hole-cue { left: 40px; gap: 8px; }
  .cue-text { font-size: 1rem; }
}
</style>
