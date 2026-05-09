'use client';

import { buttonClassName } from '@/components/Button';
import { Eyebrow } from '@/components/Eyebrow';
import { useState } from 'react';

// Demo reservation form. Per architecture.md § 8 the production form
// posts via server action → Resend; this implementation keeps state
// client-side and shows the confirm view inline so the demo flow is
// self-contained until Resend is wired in.

type Locale = 'pt' | 'en';

const STRINGS = {
  pt: {
    reservationsLabel: 'Reservas',
    confirmedLabel: 'Reserva confirmada',
    title: { before: 'Uma mesa em ', accent: 'Anjos.' },
    lead: 'As reservas são feitas apenas em Anjos — as outras duas lojas operam só ao balcão. Ter–Dom, brunch das 8h30 às 12h30.',
    seeYou: { before: 'Vemo-nos no ', accent: 'domingo.' },
    fields: {
      store: 'Loja',
      date: 'Data',
      time: 'Hora',
      party: 'Pessoas',
      name: 'Nome',
      phone: 'Telefone',
    },
    placeholders: { name: 'O seu nome', phone: '+351' },
    submit: 'Reservar mesa',
    fineprint: 'Sem cartão · cancele até 2h antes',
    nextLabel: 'O que se segue',
    next: 'A confirmação chegará ao número que indicou. Cancele até 2h antes — sem cartão.',
    again: 'Fazer outra',
    counterOnly: ' — só ao balcão',
    guests: (n: number) => `${n} ${n === 1 ? 'pessoa' : 'pessoas'}`,
  },
  en: {
    reservationsLabel: 'Reservations',
    confirmedLabel: 'Reservation confirmed',
    title: { before: 'A table at ', accent: 'Anjos.' },
    lead: 'Reservations are taken at Anjos only — the other two stores run counter-only. Tue–Sun, brunch service from 8:30 to 12:30.',
    seeYou: { before: 'See you ', accent: 'on Sunday.' },
    fields: {
      store: 'Store',
      date: 'Date',
      time: 'Time',
      party: 'Party',
      name: 'Name',
      phone: 'Phone',
    },
    placeholders: { name: 'Your name', phone: '+351' },
    submit: 'Reserve a table',
    fineprint: 'No card required · cancel up to 2h before',
    nextLabel: 'What happens next',
    next: 'A confirmation will arrive at the number you gave us. Cancel up to 2 hours before — no card needed.',
    again: 'Make another',
    counterOnly: ' — counter only',
    guests: (n: number) => `${n} ${n === 1 ? 'guest' : 'guests'}`,
  },
} as const;

const TIME_SLOTS = ['08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00'];

export function ReservationForm({ locale }: { locale: Locale }) {
  const t = STRINGS[locale];
  const [step, setStep] = useState<'form' | 'confirmed'>('form');
  const [form, setForm] = useState({
    store: 'Anjos',
    date: '2026-05-17',
    time: '10:00',
    party: 2,
    name: '',
    phone: '',
  });

  if (step === 'confirmed') {
    return (
      <div className="text-center pt-22 pb-30">
        <Eyebrow>{t.confirmedLabel}</Eyebrow>
        <h1 className="display-lg mt-3.5 mb-4">
          {t.seeYou.before}
          <em>{t.seeYou.accent}</em>
        </h1>
        <p
          className="text-[22px] mt-0 mb-9"
          style={{
            fontFamily: 'var(--font-serif-accent)',
            fontStyle: 'italic',
            color: 'var(--color-gold)',
          }}
        >
          {t.guests(form.party)} · {form.date} · {form.time} · {form.store}
        </p>
        <div
          className="text-left max-w-[480px] mx-auto p-6 border border-[rgba(26,22,19,0.14)]"
          style={{ background: 'var(--color-paper-2)' }}
        >
          <Eyebrow className="block mb-2">{t.nextLabel}</Eyebrow>
          <p className="m-0 text-[14px] text-[color:var(--color-ink-2)] leading-[1.5]">{t.next}</p>
        </div>
        <button
          type="button"
          onClick={() => setStep('form')}
          className={buttonClassName({ variant: 'ghost', className: 'mt-9' })}
        >
          {t.again}
        </button>
      </div>
    );
  }

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        setStep('confirmed');
      }}
      className="p-5 sm:p-8 border border-[rgba(26,22,19,0.14)]"
      style={{ background: 'var(--color-paper-2)' }}
    >
      <Field label={t.fields.store} htmlFor="rsvp-store">
        <select
          id="rsvp-store"
          value={form.store}
          onChange={(e) => setForm((f) => ({ ...f, store: e.target.value }))}
          className={selectClass}
        >
          <option value="Anjos">Anjos</option>
          <option disabled>Campo de Ourique{t.counterOnly}</option>
          <option disabled>Beato{t.counterOnly}</option>
        </select>
      </Field>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Field label={t.fields.date} htmlFor="rsvp-date">
          <input
            id="rsvp-date"
            type="date"
            value={form.date}
            onChange={(e) => setForm((f) => ({ ...f, date: e.target.value }))}
            className={inputClass}
          />
        </Field>
        <Field label={t.fields.time} htmlFor="rsvp-time">
          <select
            id="rsvp-time"
            value={form.time}
            onChange={(e) => setForm((f) => ({ ...f, time: e.target.value }))}
            className={selectClass}
          >
            {TIME_SLOTS.map((slot) => (
              <option key={slot}>{slot}</option>
            ))}
          </select>
        </Field>
        <Field label={t.fields.party} htmlFor="rsvp-party">
          <input
            id="rsvp-party"
            type="number"
            min={1}
            max={8}
            value={form.party}
            onChange={(e) => setForm((f) => ({ ...f, party: Number(e.target.value) }))}
            className={inputClass}
          />
        </Field>
      </div>

      <Field label={t.fields.name} htmlFor="rsvp-name">
        <input
          id="rsvp-name"
          type="text"
          value={form.name}
          onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
          placeholder={t.placeholders.name}
          required
          className={inputClass}
        />
      </Field>

      <Field label={t.fields.phone} htmlFor="rsvp-phone">
        <input
          id="rsvp-phone"
          type="tel"
          value={form.phone}
          onChange={(e) => setForm((f) => ({ ...f, phone: e.target.value }))}
          placeholder={t.placeholders.phone}
          required
          className={inputClass}
        />
      </Field>

      <div className="mt-6">
        <button
          type="submit"
          className={buttonClassName({ variant: 'ember', className: 'w-full' })}
        >
          {t.submit}
        </button>
      </div>
      <p className="text-[12px] text-[color:var(--color-stone)] text-center m-0 mt-4">
        {t.fineprint}
      </p>
    </form>
  );
}

const inputClass =
  'w-full bg-[color:var(--color-paper)] border border-[rgba(26,22,19,0.28)] text-[color:var(--color-ink)] py-[13px] px-[14px] font-[family-name:var(--font-body)] text-[15px] rounded-[4px] outline-none focus:border-[color:var(--color-ember)] transition-colors box-border';

const selectClass = `${inputClass} appearance-none bg-[image:linear-gradient(45deg,transparent_50%,var(--color-ink)_50%),linear-gradient(135deg,var(--color-ink)_50%,transparent_50%)] bg-[position:calc(100%-18px)_calc(50%-2px),calc(100%-13px)_calc(50%-2px)] bg-[size:5px_5px,5px_5px] bg-no-repeat`;

function Field({
  label,
  htmlFor,
  children,
}: {
  label: string;
  htmlFor: string;
  children: React.ReactNode;
}) {
  return (
    <div className="block mb-4">
      <label htmlFor={htmlFor} className="block">
        <Eyebrow className="block mb-1.5 text-[color:var(--color-stone)]">{label}</Eyebrow>
      </label>
      {children}
    </div>
  );
}
