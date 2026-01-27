# 🎨 What kind of animations ragflow.io uses

## 🟦 1. **Lottie animations (very likely)**
Many of the smooth looping illustrations on the site resemble **Lottie** files.  
Lottie is a lightweight animation format exported from **Adobe After Effects** using the **Bodymovin** plugin.

### Why this fits what you see:
- Smooth vector animation  
- No pixelation at any size  
- Very small file size  
- Transparent backgrounds  
- Runs via JavaScript (`lottie-web`)  

### How they’re created:
1. Designer animates in **Adobe After Effects**  
2. Export using **Bodymovin** → produces a `.json` animation file  
3. Developer embeds it using:
   ```js
   lottie.loadAnimation({
     container: document.getElementById('anim'),
     renderer: 'svg',
     loop: true,
     autoplay: true,
     path: 'animation.json'
   });
   ```

---

## 🟩 2. **CSS + JavaScript animations**
Some UI elements (hover effects, fades, slides) are done with CSS transitions or libraries like:
- GSAP (GreenSock)
- Framer Motion
- Tailwind CSS animations

These handle:
- Smooth fades  
- Sliding text  
- Element transitions  

Example:
```css
.fade-in {
  animation: fade 1.2s ease-in-out forwards;
}

@keyframes fade {
  from { opacity: 0; }
  to   { opacity: 1; }
}
```

---

## 🟥 3. **WebM/MP4 looping videos (sometimes used)**
Some hero sections on modern SaaS sites use **silent looping videos** instead of GIFs because:
- Much smaller file size  
- Full color  
- High frame rate  

But ragflow.io seems to rely more on vector animations than video.

---

# 🧪 How to confirm (if you want to check yourself)
If you open **Developer Tools → Network → filter “.json”**, you’ll often see files like:

```
hero-animation.json
workflow-animation.json
```

These are Lottie files.

---

# 🛠️ Want to create similar animations?
You can build them using:

### **Design tools**
- Adobe After Effects + Bodymovin (most common)
- Figma + Lottie plugins
- Rive (interactive vector animations)

### **Web integration**
- `lottie-web` (JS)
- React: `lottie-react`
- Vue: `vue-lottie`
- Svelte: `svelte-lottie`

---

If you want, I can walk you through **how to make your own Lottie animation**, or even help you design one step‑by‑step.
