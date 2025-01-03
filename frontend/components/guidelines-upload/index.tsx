"use client";

import { useDashboard} from "@/context/dashboard-context";
import classNames from "classnames";
import { FaCheck, FaSpinner } from "react-icons/fa";
import { useState } from "react";

export default function GuidelinesUpload() {
    const [isLoading, setIsLoading] = useState(false);
    const { guidelinesFile, setGuidelinesFile } = useDashboard();

    const handleClick = () => {
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
                    guidelinesFile === null ? "bg-orange-500 border-orange-500" : "border-transparent text-green-600" 
                )}
                onClick={handleClick}
                disabled={isLoading}
            >
                {isLoading ? (
                    <>
                        <FaSpinner className="animate-spin h-5 w-5" />
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