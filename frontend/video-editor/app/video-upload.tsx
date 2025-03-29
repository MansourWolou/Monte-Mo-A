"use client";

import type React from "react";
import { useState, useRef } from "react";
import { useRouter } from "next/navigation"; // Import useRouter
import Image from "next/image";
import { ArrowDown } from "lucide-react";

const scaleInAnimation = `
  @keyframes scaleIn {
    0% {
      transform: scale(0.85);
      opacity: 0.7;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }
`;

export default function VideoUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isHovered, setIsHovered] = useState(false);
  const router = useRouter(); // Initialize the router

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type.startsWith("video/")) {
        setFile(droppedFile);
        router.push("/"); // Navigate to the main page
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      router.push("/"); // Navigate to the main page
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <>
      <style jsx global>
        {scaleInAnimation}
      </style>
      <div className="flex flex-col items-center justify-center min-h-screen bg-[#ffffff] p-4">
        <div className="mb-4">
          <Image src="/assets/logo.png" alt="Play icon" width={120} height={120} />
        </div>

        <h2 className="text-[#000000] text-xl mb-6">Upload vidéo</h2>

        <div
          className={`w-full max-w-3xl h-52 rounded-2xl bg-[#f0f0f0] flex items-center justify-center cursor-pointer transition-all duration-300 animate-[scaleIn_0.6s_ease-out] origin-center ${
            isDragging ? "border-2 border-dashed border-gray-400" : ""
          } ${isHovered ? "transform scale-105" : "transform scale-100"}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleClick}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
        >
          {file ? (
            <p className="text-gray-700">Selected: {file.name}</p>
          ) : (
            <div className="flex flex-col items-center">
              <ArrowDown className="w-10 h-10 text-gray-500 mb-3" />
              <div className="w-16 h-4 rounded-full overflow-hidden mb-3">
                <Image
                  src="/placeholder.svg?height=16&width=64"
                  alt="Bar"
                  width={64}
                  height={16}
                  className="w-full h-full object-cover"
                />
              </div>
              <input type="file" ref={fileInputRef} className="hidden" accept="video/*" onChange={handleFileChange} />
            </div>
          )}
        </div>
      </div>
    </>
  );
}

