'use client';

import { useState } from 'react';
import { uploadCsvAndExtractClaims, verifyClaims } from '@/lib/claimApi';
import { ExtractedClaim, VerificationReport } from '@/lib/types';

export default function HomePage() {
  const [claims, setClaims] = useState<ExtractedClaim[]>([]);
  const [report, setReport] = useState<VerificationReport | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setLoading(true);
      const extracted = await uploadCsvAndExtractClaims(file);
      setClaims(extracted);
      setLoading(false);
    }
  };

  const handleVerify = async () => {
    setLoading(true);
    const result = await verifyClaims(claims);
    setReport(result);
    setLoading(false);
  };

  return (
    <main className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">🕵️ Claim Verification Dashboard</h1>

      <input type="file" accept=".csv" onChange={handleUpload} className="mb-4" />

      {claims.length > 0 && (
        <>
          <button
            onClick={handleVerify}
            className="px-4 py-2 bg-blue-600 text-white rounded mb-4 hover:bg-blue-700"
          >
            Verify {claims.length} Claims
          </button>

          <ul className="mb-6">
            {claims.map(claim => (
              <li key={claim.claim_id} className="mb-2 border-b pb-2">
                <span className="font-medium">{claim.text}</span>
                <div className="text-sm text-gray-500">Type: {claim.claim_type} | Confidence: {claim.confidence}</div>
              </li>
            ))}
          </ul>
        </>
      )}

      {loading && <p className="text-gray-700">Processing...</p>}

      {report && (
        <section>
          <h2 className="text-2xl font-semibold mb-2">📝 Report Summary</h2>
          <pre className="bg-gray-100 p-4 rounded overflow-x-auto text-sm">
            {JSON.stringify(report.summary, null, 2)}
          </pre>
        </section>
      )}
    </main>
  );
}
