
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import FileUploader from "@/components/FileUploader";

const Home = () => {
  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
      <div className="w-full">
      
      <div className="flex items-center justify-center p-5">
        <video 
          src="./assets/logo.mp4" 
          autoPlay 
          muted // Add muted attribute to enable autoplay
          playsInline // Add playsInline for iOS support
          loop 
          className="h-60"
        ></video>
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
