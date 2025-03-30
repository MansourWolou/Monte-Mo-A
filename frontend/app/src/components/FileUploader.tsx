
import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { Upload, FileText, ArrowDownToLine } from "lucide-react";
import { useFile } from "@/contexts/FileContext";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

const FileUploader = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const { setUploadedFile, setFilePreview } = useFile();
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);
      
      const files = e.dataTransfer.files;
      if (files.length) {
        handleFileUpload(files[0]);
      }
    },
    []
  );

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files?.length) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileUpload = (file: File) => {
    setIsUploading(true);
    setUploadProgress(0);
    
    // Create file preview for images
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setFilePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
      const formData = new FormData();
      formData.append("file", file);
      fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Upload failed");
          }
          return response.json();
        })
    } else {
      setFilePreview(null);
    }

    // Simulate upload with progress
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsUploading(false);
          setUploadedFile(file);
          
          toast({
            title: "Upload Complete",
            description: `${file.name} has been uploaded successfully.`,
          });
          
          navigate("/search");  // Changed from "/file-details" to "/search"
          return 100;
        }
        return prev + 10;
      });
    }, 300);
  };

  return (
    <div className="w-full max-w-xl mx-auto hover:scale-105 transition-transform">

    {isUploading && (
        <div className="m-8">
          <Progress value={uploadProgress} className="h-9 bg-[url('/assets/bg1upscale.png')] " >
          </Progress>
        </div>
      )}

      
      {!isUploading && (
        <div
          className={`border-2 bg-gray-200 shadow-md rounded-lg p-32 text-center cursor-pointer transition-all ${
            isDragging
              ? "border-gray-300 -500 bg-blue-50"
              : "border-gray-300 hover:border-gray-400"
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById("file-input")?.click()}
        >
          <input
            id="file-input"
            type="file"
            className="hidden"
            onChange={handleFileChange}
          />
          <ArrowDownToLine className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">
            {isDragging ? "Drop your file here" : ""}
          </h3>
          <div className="flex w-full items-center justify-center">
            <div className="w-24 h-3 bg-[url('./assets/bg1upscale.png')] bg-cover bg-center bg-no-repeat rounded-xl flex items-center justify-center"></div>
          </div>
        </div>
      )}
      
      
    </div>
  );
};

export default FileUploader;
