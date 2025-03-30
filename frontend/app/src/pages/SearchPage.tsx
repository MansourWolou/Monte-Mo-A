import { useState } from "react";
import { useNavigate } from "react-router-dom";

const SearchPage = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would typically handle the search logic
    // For now, we'll just redirect to file-details
    navigate("/file-details");
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
  



      <div className="flex flex-col items-center justify-center min-h-screen py-12 px-4">
      {/* Logo */}
      <div className="mb-12">
      <video 
            src="./assets/logo.mp4" 
            autoPlay 
            muted
            playsInline
            loop
            className="aspect-square w-full max-w-[200px] box-border"
          />
      </div>

      {/* Image Gallery */}
      <div className="w-full max-w-3xl bg-[#ffad72] rounded-3xl py-4 px-12 mb-10  bg-cover bg-[url(/assets/bg1upscaleH-max1024.png)]">
        <div className="flex flex-row justify-between gap-6">
          {[1, 2, 3].map((item) => (
            <div key={item} className="rounded-xl overflow-hidden border-4 border-white aspect-video">
              <img
                src="/placeholder.svg?height=169&width=300"
                alt={`Gallery image ${item}`}
                width={300}
                height={169}
                className="w-full h-full object-cover"
              />
            </div>
          ))}
        </div>
      </div>
      <div className="w-full max-w-md">
            {/* Search Form */}
        <form onSubmit={handleSearch} className="space-y-4">
          <textarea
        
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search..."
            className="w-full py-3 px-4 pr-12 rounded-[20px] bg-[#ece6f0] text-[#49454f] placeholder-[#49454f] focus:outline-none resize-y min-h-[48px] max-h-[200px] overflow-auto"
            style={{
              overflowY: "hidden",
              height: "auto",
            }}
            onInput={(e) => {
              const target = e.target as HTMLTextAreaElement
              target.style.height = "auto"
              target.style.height = `${target.scrollHeight}px`
            }}
          />
          <button
            type="submit"
            className="w-full max-w-32 mx-auto flex justify-center items-center py-1 px-8 rounded-full bg-[#ff9775] text-white font-bold text-3x1 hover:bg-opacity-90 transition-colors bg-[url(/assets/bg1upscale.png)]"
          >
            Search
          </button>
        </form>
      </div>
    </div>
    

    </div>



  );
};

export default SearchPage;