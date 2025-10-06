import Link from "next/link";

const Homepage = () => {
  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-semibold">Hospital Management System</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <Link href="/patients" className="border rounded p-4 hover:bg-gray-50">Patients</Link>
        <Link href="/departments" className="border rounded p-4 hover:bg-gray-50">Departments</Link>
        <Link href="/appointments" className="border rounded p-4 hover:bg-gray-50">Appointments</Link>
      </div>
      <p className="text-gray-500 text-sm">Backend proxied at /api → FastAPI on :8000</p>
    </div>
  );
};

export default Homepage