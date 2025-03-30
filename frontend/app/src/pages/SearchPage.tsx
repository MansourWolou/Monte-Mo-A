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

        What DO you want to know about this video?


        {/* Image Gallery */}
        <div className="w-full max-w-3xl bg-[#ffad72] rounded-3xl py-4 px-12 mb-1 bg-cover bg-[url(/assets/bg1upscaleH-max1024.png)]">
          <div className="flex flex-row justify-between gap-6">
            {[
              "../public/assets/video-preview-analysis/highlight_extra_1.jpg",
              "../public/assets/video-preview-analysis/highlight_extra_2.jpg",
              "../public/assets/video-preview-analysis/highlight_extra_3.jpg",
            ].map((src, index) => (
              <div key={index} className="rounded-xl overflow-hidden border-4 border-white aspect-video">
                <img
                  src={src}
                  alt={`Gallery image ${index + 1}`}
                  height={70}
                  className="w-full h-full object-cover"
                />
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-row gap-4 w-full my-4">
          <button
            type="submit"
            className="flex-1 flex justify-left py-4 px-8 rounded-full bg-gray-300 text-gray-700 font-bold text-3x1 hover:bg-gray-900 hover:text-gray-100 transition-colors"
          >
            Was anything filmed during the cocktail hour?
          </button>
          <button
            type="submit"
            className="flex-1 flex justify-left py-4 px-8 rounded-full bg-gray-300 text-gray-700 font-bold text-3x1 hover:bg-gray-900 hover:text-gray-100 transition-colors"
          >
            Could we highlight that candid moment with the flower girl dancing alone?
          </button>
          <button
            type="submit"
            className="flex-1 flex justify-left py-4 px-8 rounded-full bg-gray-300 text-gray-700 font-bold text-3x1 hover:bg-gray-900 hover:text-gray-100 transition-colors"
          >
            Can we keep that moment where they're reading their vows and start crying?
          </button>
        </div>

        <div className="text-gray-700 mb-3">or</div>

        <div className="w-full max-w-3xl">
          {/* Search Form */}
          <form onSubmit={handleSearch} className="space-y-4">
            <textarea

              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Give me all the rushes about people smiling..."
              className="w-full py-3 px-4 pr-12 rounded-[20px] bg-[#ece6f0] text-[#49454f] placeholder-[#49454f] focus:outline-none resize-y min-h-[100px] max-h-[230px] overflow-auto"
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
              className="w-full  mx-auto flex justify-center items-center py-4 px-8 rounded-full bg-black text-white font-bold text-3x1 hover:bg-opacity-90 transition-colors"
            >
              De-rush !
            </button>
          </form>
        </div>
      </div>


    </div>



  );
};

export default SearchPage;