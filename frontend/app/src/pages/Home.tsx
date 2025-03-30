
import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import FileUploader from "@/components/FileUploader";

const Home = () => {
  const [showSplash, setShowSplash] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowSplash(false);
    }, 3000);
    return () => clearTimeout(timer);
  }, []);

  if (showSplash) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center">
        <video 
          src="../public/assets/video1_Noir.mp4" 
          autoPlay 
          muted
          playsInline
          className="w-full h-full object-cover"
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
      <div className="w-full">
        <div className="flex items-center justify-center p-5">
          <video 
            src="./assets/logo.mp4" 
            autoPlay 
            muted
            playsInline
            loop
            className="aspect-square w-full max-w-lg box-border"
          />
        </div>
        <Card>
          <CardContent>
            <FileUploader />
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Home;
