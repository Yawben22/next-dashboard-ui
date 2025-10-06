"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Appointment = { id: number; patient_id: number; doctor_id: number; scheduled_for: string; status: string };

export default function AppointmentsPage() {
  const [items, setItems] = useState<Appointment[]>([]);
  useEffect(() => {
    (async () => {
      const res = await api<Appointment[]>("/appointments");
      if (res.ok) setItems(res.data);
    })();
  }, []);
  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Appointments</h1>
      <ul className="space-y-2">
        {items.map((a) => (
          <li key={a.id} className="p-3 rounded border">
            <div className="font-medium">{new Date(a.scheduled_for).toLocaleString()}</div>
            <div className="text-sm text-gray-500">Patient #{a.patient_id} · Doctor #{a.doctor_id} · {a.status}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
