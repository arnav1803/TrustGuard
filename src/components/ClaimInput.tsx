// src/components/ClaimList.tsx
import { ExtractedClaim } from "@/lib/types";

export default function ClaimList({ claims }: { claims: ExtractedClaim[] }) {
  return (
    <ul className="mb-6">
      {claims.map((claim) => (
        <li key={claim.claim_id} className="mb-2 border-b pb-2">
          <span className="font-medium">{claim.text}</span>
          <div className="text-sm text-gray-500">
            Type: {claim.claim_type} | Confidence: {claim.confidence}
          </div>
        </li>
      ))}
    </ul>
  );
}
// src/components/ClaimInput.tsx
export default function ClaimInput({ onUpload }: { onUpload: (file: File) => void }) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onUpload(file);
  };

  return (
    <input
      type="file"
      accept=".csv"
      onChange={handleChange}
      className="mb-4"
    />
  );
}
