"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Patient = {
  id: number;
  first_name: string;
  last_name: string;
  email?: string | null;
  phone?: string | null;
};

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const res = await api<Patient[]>("/patients");
      if (res.ok) setPatients(res.data);
      setLoading(false);
    })();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Patients</h1>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="space-y-2">
          {patients.map((p) => (
            <div key={p.id} className="p-3 rounded border flex justify-between">
              <div>
                <div className="font-medium">{p.first_name} {p.last_name}</div>
                <div className="text-sm text-gray-500">{p.email || "-"} · {p.phone || "-"}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
