import { VerificationReport } from "@/lib/types";

export default function SummaryReport({ report }: { report: VerificationReport }) {
  return (
    <section>
      <h2 className="text-2xl font-semibold mb-2">📝 Report Summary</h2>
      <pre className="bg-gray-100 p-4 rounded overflow-x-auto text-sm">
        {JSON.stringify(report.summary, null, 2)}
      </pre>
    </section>
  );
}