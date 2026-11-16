// Encabezado del inicio: rota los lanzamientos destacados cada 10 segundos.
// Se pausa con el mouse encima, al enfocar con teclado, con el botón de pausa
// y si la persona tiene activado "reducir movimiento" en su dispositivo.

const carrusel = document.querySelector(".hero-carrusel");

if (carrusel) {
  const diapos = [...carrusel.querySelectorAll(".hero-diapo")];
  const puntos = [...carrusel.querySelectorAll(".hero-punto")];
  const pausa = carrusel.querySelector(".hero-pausa");
  const SEGUNDOS = 10;
  const HERO_EN = document.documentElement.lang === "en";
  const TXT = HERO_EN ? { pausar: "Pause", seguir: "Play" } : { pausar: "Pausar", seguir: "Reproducir" };

  let actual = 0;
  let reloj = null;
  let pausadoPorUsuario = matchMedia("(prefers-reduced-motion: reduce)").matches;

  function mostrar(n) {
    actual = (n + diapos.length) % diapos.length;
    diapos.forEach((d, i) => {
      const activa = i === actual;
      d.classList.toggle("activa", activa);
      d.setAttribute("aria-hidden", String(!activa));
      d.inert = !activa;
    });
    puntos.forEach((p, i) => p.setAttribute("aria-current", i === actual ? "true" : "false"));
  }

  function arrancar() {
    detener();
    if (!pausadoPorUsuario && diapos.length > 1) reloj = setInterval(() => mostrar(actual + 1), SEGUNDOS * 1000);
  }

  function detener() {
    clearInterval(reloj);
    reloj = null;
  }

  function pintarPausa() {
    pausa.textContent = pausadoPorUsuario ? "▶" : "❚❚";
    pausa.setAttribute("aria-label", pausadoPorUsuario ? TXT.seguir : TXT.pausar);
  }

  puntos.forEach((p, i) => p.addEventListener("click", () => { mostrar(i); arrancar(); }));
  pausa.addEventListener("click", () => {
    pausadoPorUsuario = !pausadoPorUsuario;
    pintarPausa();
    arrancar();
  });

  carrusel.addEventListener("mouseenter", detener);
  carrusel.addEventListener("mouseleave", arrancar);
  carrusel.addEventListener("focusin", detener);
  carrusel.addEventListener("focusout", (e) => { if (!carrusel.contains(e.relatedTarget)) arrancar(); });

  mostrar(0);
  pintarPausa();
  arrancar();
}
