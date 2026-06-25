import { ref, onMounted, onUnmounted } from 'vue'

/** IntersectionObserver：元素进入视口时触发（React Bits FadeContent / BlurText 同款思路） */
export function useInView(options = {}) {
  const { threshold = 0.12, rootMargin = '0px', once = true } = options
  const targetRef = ref(null)
  const inView = ref(false)

  let observer = null

  onMounted(() => {
    const el = targetRef.value
    if (!el) return

    observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          inView.value = true
          if (once) observer?.unobserve(el)
        } else if (!once) {
          inView.value = false
        }
      },
      { threshold, rootMargin },
    )
    observer.observe(el)
  })

  onUnmounted(() => observer?.disconnect())

  return { targetRef, inView }
}
