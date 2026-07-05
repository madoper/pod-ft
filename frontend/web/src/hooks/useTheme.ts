import { useCallback, useSyncExternalStore } from "react";

function getTheme(): "light" | "dark" {
  return (document.documentElement.getAttribute("data-theme") as "light" | "dark") || "light";
}

function setTheme(theme: "light" | "dark") {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme", theme);
}

function subscribe(cb: () => void) {
  const observer = new MutationObserver(() => cb());
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  return () => observer.disconnect();
}

function getSnapshot(): "light" | "dark" {
  return getTheme();
}

function getServerSnapshot(): "light" | "dark" {
  return "light";
}

export function useTheme() {
  const theme = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
  const isDark = theme === "dark";

  const toggleTheme = useCallback(() => {
    setTheme(isDark ? "light" : "dark");
  }, [isDark]);

  const setThemeLight = useCallback(() => setTheme("light"), []);
  const setThemeDark = useCallback(() => setTheme("dark"), []);

  return { theme, isDark, toggleTheme, setThemeLight, setThemeDark } as const;
}
