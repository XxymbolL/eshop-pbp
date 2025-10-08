function showToast(text = 'Saved', duration = 2500){
  const t = document.getElementById('toast');
  const s = document.getElementById('toast-text');
  if(!t || !s) return;
  s.textContent = text;
  t.classList.remove('opacity-0','translate-y-6');
  t.classList.add('opacity-100','translate-y-0');
  setTimeout(()=>{
    t.classList.add('opacity-0','translate-y-6');
    t.classList.remove('opacity-100','translate-y-0');
  }, duration);
}
