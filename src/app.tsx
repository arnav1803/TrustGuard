import React, { useState } from 'react';
import ClaimInput from './components/ClaimInput';
import ExtractedClaimsList from './components/ExtractedClaimsList';
import VerificationResultCard from './components/VerificationResultCard';
import ReportViewer from './components/ReportViewer';
import { extractClaims, verifyClaims, fetchReport } from './api/claimApi';
import { ExtractedClaim, VerificationResult } from './types/types';

function App() {
  const [inputText, setInputText] = useState('');
  const [claims, setClaims] = useState<ExtractedClaim[]>([]);
  const [results, setResults] = useState<VerificationResult[]>([]);
  const [report, setReport] = useState<any>(null);

  const handleExtract = async () => {
    const extracted = await extractClaims(inputText);
    setClaims(extracted);
  };

  const handleVerify = async () => {
    const verified = await verifyClaims(claims);
    setResults(verified);
    const generatedReport = await fetchReport(verified);
    setReport(generatedReport);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        <ClaimInput text={inputText} setText={setInputText} onExtract={handleExtract} />
        <ExtractedClaimsList claims={claims} />
        <div className="space-y-4">
          {results.map((result) => (
            <VerificationResultCard key={result.claim_id} result={result} />
          ))}
        </div>
        {results.length > 0 && (
          <button
            onClick={handleVerify}
            className="bg-blue-600 text-white px-4 py-2 rounded shadow"
          >
            Run Verification
          </button>
        )}
        {report && <ReportViewer report={report} />}
      </div>
    </div>
  );
}

export default App;
