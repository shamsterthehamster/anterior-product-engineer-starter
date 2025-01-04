"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import classNames from "classnames";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";
import Link from "next/link";

export default function CaseResult({ params }: { params: { case_id: string } }) {
	const [caseData, setCaseData] = useState<any>(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);
	const [showSteps, setShowSteps] = useState(false);
	const router = useRouter();

	const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
	const toggleSteps = () => setShowSteps(!showSteps);

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
	if (error) return (
		<div className="h-screen flex flex-col justify-center items-center">
			{/* Error Box */}
			<div className="w-full max-w-md p-6 bg-red-100 border-l-4 border-red-500 text-red-700 rounded-md shadow-lg">
				<h2 className="text-lg font-semibold">⚠️ Something went wrong</h2>
				<p className="mt-2">{error}</p>
			</div>

			{/* navigate back to dashboard */}
			<p className="mt-4">
				<Link href="/dashboard" className="text-blue-600 font-semibold hover:underline">
					Back to Dashboard
				</Link>
			</p>
		</div>
	);
	
	return (
        <div className="max-w-2xl mx-auto mt-10 p-6 bg-white shadow-lg rounded-lg">
            <h1 className="text-3xl font-bold text-gray-800 mb-4 text-center">Case Details</h1>

			{/*Case Status*/}
			<div
                className={classNames(
                    "text-white text-sm font-semibold px-4 py-2 rounded-full w-fit mx-auto",
                    caseData.status === "submitted" ? "bg-blue-500" :
                    caseData.status === "processing" ? "bg-yellow-500" :
                    "bg-green-500"
                )}
            >
                {caseData.status.toUpperCase()}
            </div>

			<div className="mt-6 space-y-4">
                <div className="flex justify-between">
                    <p className="text-gray-700 font-bold">Case ID:</p>
                    <p className="text-gray-900">{caseData.case_id}</p>
                </div>

                {caseData.status === "complete" && (
                    <>
                        <div className="flex justify-between">
                            <p className="text-gray-700 font-bold">Procedure Name:</p>
                            <p className="text-gray-900">{caseData.procedure_name || "N/A"}</p>
                        </div>
                        <div className="flex justify-between">
                            <p className="text-gray-700 font-bold">CPT Codes:</p>
                            <p className="text-gray-900">{caseData.cpt_codes?.join(", ") || "N/A"}</p>
                        </div>
                        <div className="mt-4">
                            <p className="text-gray-700 font-bold">Summary:</p>
                            <p className="text-gray-800 bg-gray-100 p-3 rounded">{caseData.summary || "N/A"}</p>
                        </div>
                        <div className="mt-4">
							<div className="flex justify-between items-center cursor-pointer" onClick={toggleSteps}>
								<p className="text-gray-700 font-bold">Steps Taken:</p>
								<button className="text-blue-500 flex items-center">
									{showSteps ? <FaChevronUp /> : <FaChevronDown />} {/* Arrow icon */}
								</button>
							</div>

							{showSteps && (
								<ul className="list-disc ml-6 text-gray-600 space-y-3 mt-2 transition-all duration-300">
									{caseData.steps?.map((step: any, index: number) => (
										<li key={index} className="bg-gray-100 p-3 rounded shadow-md">
											<p><strong>Question:</strong> {step.question}</p>
											<p><strong>Decision:</strong> {step.decision}</p>
											<p><strong>Reasoning:</strong> {step.reasoning}</p>
										</li>
									))}
								</ul>
							)}
                        </div>
                        <div className="mt-4 flex justify-between items-center">
                            <p className="text-gray-700 font-bold">Final Determination:</p>
                            <p
                                className={classNames(
                                    "font-semibold px-3 py-1 rounded-full text-white",
                                    caseData.is_met ? "bg-green-600" : "bg-red-500"
                                )}
                            >
                                {caseData.is_met ? "Met" : "Not Met"}
                            </p>
                        </div>
                    </>
                )}

                {caseData.status !== "complete" && (
                    <p className="text-gray-500 italic text-center mt-4">
                        Processing... Please check back later.
                    </p>
                )}
            </div>

            <div className="mt-6 flex justify-center">
                <button
                    className="bg-blue-600 text-white px-5 py-2 rounded-lg font-semibold hover:bg-blue-700 transition"
                    onClick={() => router.push("/dashboard")}
                >
                    Back to Dashboard
                </button>
            </div>
        </div>
    );
}
