"use client";

import { useDashboard} from "@/context/dashboard-context";
import classNames from "classnames";
import { FaCheck, FaSpinner } from "react-icons/fa";
import { useState } from "react";
import { toast } from "react-toastify";

export default function GuidelinesUpload() {
    const [isLoading, setIsLoading] = useState(false);
    const { medicalRecord, guidelinesFile, setGuidelinesFile } = useDashboard();

    const handleClick = () => {
        if (!medicalRecord) {
            toast.warning("Please upload a medical record first");
            return;
        }

        setIsLoading(true);
        setTimeout(() => {
            setIsLoading(false);
            setGuidelinesFile({ url: "/assets/guidelines.pdf" });
        }, 3000);
    }

    return(
        <div className="w-1/2 h-64 border border-4 border-gray-200 border-dashed rounded flex flex-row items-center justify-center">
            <button
                className={classNames(
                    "text-white font-medium py-2 px-4 rounded border border-2",
                    isLoading
                        ? "bg-transparent border-transparent"
                        : medicalRecord === null
                        ? "bg-gray-400 border-gray-400"
                        : (guidelinesFile === null
                            ? "bg-orange-500 border-orange-500"
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
                ) : guidelinesFile === null ? (
                    <span>Simulate Guidelines Upload</span>
                ) : (
                    <span className="text-green-600 flex flex-row gap-1 items-center">
                        <FaCheck />
                        <span>Guidelines File Uploaded</span>
                    </span>
                )}
            </button>
        </div>
    )
}