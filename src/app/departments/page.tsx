"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Department = { id: number; name: string; description?: string | null };

export default function DepartmentsPage() {
  const [items, setItems] = useState<Department[]>([]);
  useEffect(() => {
    (async () => {
      const res = await api<Department[]>("/departments");
      if (res.ok) setItems(res.data);
    })();
  }, []);
  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Departments</h1>
      <ul className="space-y-2">
        {items.map((d) => (
          <li key={d.id} className="p-3 rounded border">
            <div className="font-medium">{d.name}</div>
            <div className="text-sm text-gray-500">{d.description || "-"}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
