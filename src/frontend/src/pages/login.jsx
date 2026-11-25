import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/css/login.css";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [feedback, setFeedback] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setFeedback("");
    setSubmitting(true);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim(), password }),
      });
      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.error || "Não foi possível iniciar sessão. Tente novamente.");
      }

      if (!data.access_token) {
        throw new Error("O servidor não devolveu um token de autenticação válido.");
      }

      sessionStorage.setItem("access_token", data.access_token);
      navigate("/", { replace: true });
    } catch (error) {
      setFeedback(
        error.message || "Não foi possível ligar ao servidor. Tente novamente.",
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="login-page">
      <section className="login-card" aria-labelledby="login-title">
        <div className="login-form-panel">
          <header className="login-header">
            <div className="login-brand-mark" aria-hidden="true">A</div>
            <span className="login-eyebrow">ALFAS · LITERACIA EM SAÚDE</span>
            <h1 id="login-title">Entrar no ALFAS</h1>
            <p className="login-welcome">Bom ter-te de volta.</p>
            <p className="login-intro">
              Um espaço para compreender a saúde, ganhar confiança e acompanhar
              o que aprendes.
            </p>
          </header>

          <form className="login-form" onSubmit={handleSubmit}>
            <label className="login-field">
              Email
              <input
                type="email"
                name="email"
                autoComplete="email"
                placeholder="nome@exemplo.pt"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
                maxLength={255}
              />
            </label>

            <label className="login-field">
              Palavra-passe
              <input
                type="password"
                name="password"
                autoComplete="current-password"
                placeholder="A sua palavra-passe"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />
            </label>

            {feedback && (
              <div className="login-feedback" role="alert">
                {feedback}
              </div>
            )}

            <button className="login-submit" type="submit" disabled={submitting}>
              {submitting ? "A entrar…" : "Entrar"}
              <span aria-hidden="true">→</span>
            </button>
          </form>

          <p className="login-register">
            Ainda não tens conta? <Link to="/registar">Criar conta</Link>
          </p>
        </div>

        <aside className="login-note" aria-label="Sobre os seus dados">
          <div className="login-note-icon" aria-hidden="true">✦</div>
          <h2>Clareza em cada passo</h2>
          <p>
            Os teus dados ajudam a gerir a tua conta e a acompanhar o teu
            progresso de aprendizagem.
          </p>
          <div className="login-note-decoration" aria-hidden="true">
            <span />
            <span />
            <span />
          </div>
        </aside>
      </section>

      <footer className="login-footer">
        Aprender hoje para cuidar melhor amanhã.
      </footer>
    </main>
  );
}