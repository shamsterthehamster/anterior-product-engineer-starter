"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function CaseResult({ params }: { params: { case_id: string } }) {
	const [caseData, setCaseData] = useState<any>(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);
	const router = useRouter();

	const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

	useEffect(() => {
		async function fetchCaseData() {
			try {
				const response = await fetch(`${API_BASE_URL}/cases/${params.case_id}`);

				if (!response.ok) {
					throw new Error("Case not found");
				}
				
				const data = await response.json();
				setCaseData(data);
			} catch (error: any) {
				setError(error.message);
			} finally {
				setLoading(false);
			}
		}

		fetchCaseData();
	}, [params.case_id]);

	if (loading) return <div>Loading...</div>;
	if (error) return <div className="text-red-500">Error: {error}</div>;

	return (
        <div className="max-w-2xl mx-auto mt-10 p-6 bg-white shadow-lg rounded-lg">
            <h1 className="text-xl font-bold text-gray-800">Case Details</h1>
            <p className="text-gray-700"><strong>Case ID:</strong> {caseData.case_id}</p>
            <p className="text-gray-700"><strong>Status:</strong> {caseData.status}</p>

            {caseData.status === "completed" && (
                <>
                    <p className="text-gray-700"><strong>Procedure Name:</strong> {caseData.procedure_name || "N/A"}</p>
                    <p className="text-gray-700"><strong>CPT Codes:</strong> {caseData.cpt_codes?.join(", ") || "N/A"}</p>
                    <p className="text-gray-700"><strong>Summary:</strong> {caseData.summary || "N/A"}</p>
                    <p className="text-gray-700"><strong>Steps:</strong></p>
                    <ul className="list-disc ml-6 text-gray-600">
                        {caseData.steps?.map((step: any, index: number) => (
                            <li key={index}>
                                <p><strong>Question:</strong> {step.question}</p>
                                <p><strong>Decision:</strong> {step.decision}</p>
                                <p><strong>Reasoning:</strong> {step.reasoning}</p>
                            </li>
                        ))}
                    </ul>
                    <p className="text-gray-700"><strong>Final Determination:</strong> {caseData.is_met ? "Met" : "Not Met"}</p>
                </>
            )}

            {caseData.status !== "completed" && (
                <p className="text-gray-500 italic">Processing... Please check back later.</p>
            )}

            <button
                className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                onClick={() => router.push("/dashboard")}
            >
                Back to Dashboard
            </button>
        </div>
    );
}
