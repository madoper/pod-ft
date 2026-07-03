import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "../src/App";

describe("App", () => {
  it("renders header", () => {
    render(<App />);
    expect(screen.getByText("pod-ft")).toBeDefined();
  });

  it("shows ask tab by default", () => {
    render(<App />);
    expect(screen.getByText("Задать вопрос")).toBeDefined();
  });

  it("navigates to doc check", () => {
    render(<App />);
    const btn = screen.getByText("Проверка документа");
    btn.click();
    expect(screen.getByText("Проверка документа")).toBeDefined();
  });
});
