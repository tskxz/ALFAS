import React, { useState } from "react";
import "../styles/css/registration.css";

const SCHOOL_YEARS = Array.from({ length: 12 }, (_, index) => `${index + 1}.º ano`);
const COURSE_TYPES = ["Licenciatura", "Mestrado", "CTeSP"];

const initialForm = {
  name: "",
  email: "",
  birth_date: "",
  schoolyear: "",
  course_type: "",
  course_name: "",
  gender: "",
  password: "",
  confirmPassword: "",
  guardian_name: "",
  guardian_email: "",
  parental_consent: false,
};

function getAge(birthDate) {
  if (!birthDate) return null;

  const birth = new Date(`${birthDate}T00:00:00`);
  if (Number.isNaN(birth.getTime())) return null;

  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const birthdayHasNotPassed =
    today.getMonth() < birth.getMonth() ||
    (today.getMonth() === birth.getMonth() && today.getDate() < birth.getDate());

  if (birthdayHasNotPassed) age -= 1;
  return age;
}

function validateForm(form, isMinor) {
  const passwordIsStrong =
    form.password.length >= 8 && /[A-Za-z]/.test(form.password) && /\d/.test(form.password);

  if (!passwordIsStrong) {
    return "A palavra-passe deve ter pelo menos 8 caracteres, uma letra e um número.";
  }

  if (form.password !== form.confirmPassword) {
    return "As palavras-passes não coincidem.";
  }

  if (
    isMinor &&
    (!form.guardian_name.trim() || !form.guardian_email || !form.parental_consent)
  ) {
    return "Preencha os dados do encarregado de educação e confirme a autorização.";
  }

  if (!form.schoolyear) {
    return "Selecione o ano de escolaridade ou o tipo de curso.";
  }

  if (
    form.schoolyear === "Ensino superior" &&
    (!form.course_type || !form.course_name.trim())
  ) {
    return "Selecione o tipo de curso e indique o nome do curso.";
  }

  return null;
}

function BrandMark() {
  return <div className="brand-mark">A</div>;
}

function RegistrationHeader() {
  return (
    <header className="form-header">
      <BrandMark />
      <span className="eyebrow">ALFAS · LITERACIA EM SAÚDE</span>
      <h1 id="register-title">Crie a sua conta</h1>
      <p>Junte-se à comunidade e comece a aprender.</p>
    </header>
  );
}

function RegistrationSuccess({ message }) {
  return (
    <main className="registration-page">
      <section className="success-card" aria-labelledby="success-title">
        <BrandMark />
        <span className="eyebrow">ALFAS · LITERACIA EM SAÚDE</span>
        <div className="success-icon" aria-hidden="true">✓</div>
        <h1 id="success-title">Registo recebido</h1>
        <p>{message}</p>
        <p className="muted">Pode fechar esta página.</p>
      </section>
    </main>
  );
}

function ProfileFields({ form, onChange }) {
  const isHigherEducation = form.schoolyear === "Ensino superior";

  return (
    <div className="form-grid">
      <label className="field full">
        Nome completo
        <input
          name="name"
          autoComplete="name"
          value={form.name}
          onChange={onChange}
          required
          minLength={2}
          placeholder="O seu nome"
        />
      </label>

      <label className="field full">
        Email
        <input
          name="email"
          type="email"
          autoComplete="email"
          value={form.email}
          onChange={onChange}
          required
          placeholder="nome@exemplo.pt"
        />
      </label>

      <label className="field">
        Data de nascimento
        <input
          name="birth_date"
          type="date"
          autoComplete="bday"
          value={form.birth_date}
          onChange={onChange}
          required
          max={new Date().toISOString().slice(0, 10)}
        />
      </label>

      <label className="field">
        Ano de escolaridade
        <select name="schoolyear" value={form.schoolyear} onChange={onChange} required>
          <option value="" disabled>Selecionar</option>
          {SCHOOL_YEARS.map((year) => (
            <option key={year} value={year}>{year}</option>
          ))}
          <option value="Ensino superior">Ensino superior</option>
        </select>
      </label>

      {isHigherEducation && (
        <>
          <label className="field">
            Tipo de curso
            <select name="course_type" value={form.course_type} onChange={onChange} required>
              <option value="" disabled>Selecionar</option>
              {COURSE_TYPES.map((courseType) => (
                <option key={courseType} value={courseType}>{courseType}</option>
              ))}
            </select>
          </label>

          {form.course_type && (
            <label className="field full">
              Nome do curso
              <input
                name="course_name"
                value={form.course_name}
                onChange={onChange}
                required
                maxLength={255}
                placeholder="Ex.: Engenharia Informática"
              />
            </label>
          )}
        </>
      )}

      <label className="field">
        Género
        <select name="gender" value={form.gender} onChange={onChange} required>
          <option value="" disabled>Selecionar</option>
          <option value="Feminino">Feminino</option>
          <option value="Masculino">Masculino</option>
          <option value="Outro">Outro</option>
        </select>
      </label>

      <label className="field">
        Palavra-passe
        <input
          name="password"
          type="password"
          autoComplete="new-password"
          value={form.password}
          onChange={onChange}
          required
          minLength={8}
          placeholder="Mínimo de 8 caracteres"
          aria-describedby="password-hint"
        />
        <small id="password-hint">Pelo menos 8 caracteres, uma letra e um número.</small>
      </label>

      <label className="field">
        Confirmar palavra-passe
        <input
          name="confirmPassword"
          type="password"
          autoComplete="new-password"
          value={form.confirmPassword}
          onChange={onChange}
          required
          placeholder="Repita a palavra-passe"
        />
      </label>
    </div>
  );
}

function GuardianFields({ form, onChange }) {
  return (
    <section className="guardian-panel" aria-labelledby="guardian-title">
      <div className="panel-heading">
        <span className="panel-icon" aria-hidden="true">i</span>
        <div>
          <h2 id="guardian-title">Autorização do encarregado de educação</h2>
          <p>Como tem menos de 18 anos, precisamos da autorização do seu encarregado de educação.</p>
        </div>
      </div>

      <div className="form-grid">
        <label className="field">
          Nome do encarregado
          <input
            name="guardian_name"
            autoComplete="name"
            value={form.guardian_name}
            onChange={onChange}
            required
          />
        </label>

        <label className="field">
          Email do encarregado
          <input
            name="guardian_email"
            type="email"
            autoComplete="email"
            value={form.guardian_email}
            onChange={onChange}
            required
            placeholder="encarregado@exemplo.pt"
          />
        </label>
      </div>

      <label className="consent-check">
        <input
          type="checkbox"
          name="parental_consent"
          checked={form.parental_consent}
          onChange={onChange}
          required
        />
        <span>Confirmo que o meu encarregado de educação autorizou a criação desta conta.</span>
      </label>
    </section>
  );
}

export default function Register() {
  const [form, setForm] = useState(initialForm);
  const [feedback, setFeedback] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const age = getAge(form.birth_date);
  const isMinor = age !== null && age < 18;
  const isHigherEducation = form.schoolyear === "Ensino superior";

  function handleChange(event) {
    const { name, value, checked, type } = event.target;
    setForm((currentForm) => ({
      ...currentForm,
      [name]: type === "checkbox" ? checked : value,
      ...(name === "schoolyear" && value !== "Ensino superior"
        ? { course_type: "", course_name: "" }
        : {}),
    }));
    setFeedback(null);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setFeedback(null);

    const validationError = validateForm(form, isMinor);
    if (validationError) {
      setFeedback({ type: "error", text: validationError });
      return;
    }

    setSubmitting(true);

    try {
      const response = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: form.name.trim(),
          email: form.email.trim(),
          birth_date: form.birth_date,
          schoolyear: isHigherEducation ? form.course_type : form.schoolyear,
          course_name: isHigherEducation ? form.course_name.trim() : null,
          gender: form.gender,
          password: form.password,
          guardian_name: isMinor ? form.guardian_name.trim() : null,
          guardian_email: isMinor ? form.guardian_email.trim() : null,
          parental_consent: isMinor ? form.parental_consent : false,
        }),
      });

      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.error || "Não foi possível concluir o registo. Tente novamente.");
      }

      setSubmitted(true);
      setFeedback({ type: "success", text: data.message || "Registo concluído com sucesso." });
    } catch (error) {
      setFeedback({
        type: "error",
        text: error.message || "Não foi possível ligar ao servidor. Tente novamente.",
      });
    } finally {
      setSubmitting(false);
    }
  }

  if (submitted) {
    return <RegistrationSuccess message={feedback?.text} />;
  }

  return (
    <main className="registration-page">
      <section className="registration-card" aria-labelledby="register-title">
        <RegistrationHeader />

        <form onSubmit={handleSubmit} noValidate>
          <ProfileFields
            form={form}
            onChange={handleChange}
          />

          {isMinor && <GuardianFields form={form} onChange={handleChange} />}

          {feedback && (
            <div className={`feedback ${feedback.type}`} role="alert">
              {feedback.text}
            </div>
          )}

          <button className="submit-button" type="submit" disabled={submitting}>
            {submitting ? "A criar conta…" : "Criar conta"}
            <span aria-hidden="true">→</span>
          </button>

          <p className="legal-note">
            Ao criar conta, confirma que os dados fornecidos são corretos.
          </p>
        </form>
      </section>

      <footer className="page-footer">Aprender hoje para cuidar melhor amanhã.</footer>
    </main>
  );
}
