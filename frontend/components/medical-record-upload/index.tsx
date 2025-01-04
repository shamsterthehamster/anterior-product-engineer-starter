"use client";

import { useDashboard } from "@/context/dashboard-context";
import classNames from "classnames";
import { FaCheck, FaSpinner } from "react-icons/fa";
import { useState } from "react";

export default function MedicalRecordUpload() {
    const [isLoading, setIsLoading] = useState(false);
    const { medicalRecord, setMedicalRecord } = useDashboard();

    const handleClick = () => {
        setIsLoading(true);
        setTimeout(() => {
            setIsLoading(false);
            setMedicalRecord({ url: "/assets/medical-record.pdf" });
        }, 3000);
    }

    return(
        <div className="w-1/2 h-64 border border-4 border-gray-200 border-dashed rounded flex flex-row items-center justify-center">
            <button
                className={classNames(
                    "text-white font-medium py-2 px-4 rounded border border-2",
                    isLoading 
                        ? "bg-transparent border-transparent" 
                        : (medicalRecord === null 
                            ? "bg-blue-500 border-blue-500" 
                            : "border-transparent text-green-600" 
                        )
                )}
                onClick={handleClick}
                disabled={isLoading}
            >
                {isLoading ? (
                    <>
                        <FaSpinner className="animate-spin h-7 w-7 text-gray-500" />
                    </>
                ) : medicalRecord === null ? (
                    <span>Simulate Medical Record Upload</span>
                ) : (
                    <span className="text-green-600 flex flex-row gap-1 items-center">
                        <FaCheck />
                        <span>Medical Record Uploaded</span>
                    </span>
                )}
            </button>
        </div>
    )
}