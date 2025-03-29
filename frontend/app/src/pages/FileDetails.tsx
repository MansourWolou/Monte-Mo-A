import { useState } from "react"
import { ArrowRight } from "lucide-react"

const FileDetails = () => {

  // State to track which videos have been added to the right panel
  const [addedVideos, setAddedVideos] = useState<number[]>([])

  // Sample video data
  const videos = [
    {
      id: 1,
      timestamp: "00:00:05:19",
      thumbnail: "/placeholder.svg?height=80&width=144",
      alt: "City street with red bus",
      summary:
        "Une rue animée en ville avec des gens qui marchent, des voitures qui passent et de grands immeubles en arrière-plan. La scène est dynamique avec un mélange d'architecture moderne et classique",
    },
    {
      id: 2,
      timestamp: "00:00:05:19",
      thumbnail: "/placeholder.svg?height=80&width=144",
      alt: "Forest path",
      summary:
        "Un chemin forestier serein avec la lumière du soleil filtrant à travers les arbres, créant des ombres mouchetées sur le sol. Le chemin est bordé de verdure luxuriante et de fleurs sauvages.",
    },
    {
      id: 3,
      timestamp: "00:00:05:19",
      thumbnail: "/placeholder.svg?height=80&width=144",
      alt: "Person reading",
      summary:
        "Une scène intérieure chaleureuse avec une personne lisant un livre près d'une cheminée. La pièce est doucement éclairée avec des couleurs chaudes et accueillantes, et une tasse de thé repose sur une table à proximité",
    },
  ]

  // Function to toggle adding/removing a video to/from the right panel
  const handleAddToMontage = (videoId: number) => {
    if (addedVideos.includes(videoId)) {
      // Remove the video if it's already added
      setAddedVideos(addedVideos.filter((id) => id !== videoId))
    } else {
      // Add the video if it's not already added
      setAddedVideos([...addedVideos, videoId])
    }
  }

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-white">
      {/* Blue background */}
      
      <div className="absolute inset-0 z-0 bg-White"></div>
  
      {/* Logo */}
      <div className="absolute left-12 top-12 z-10 h-24 w-24">
        
      </div>

      {/* Main content */}
      <div className="relative z-10 mx-auto max-w-6xl px-4 py-24">
      <div className="absolute left-[100px] inset-y-0  w-36  bg-sky-200 bg-[url(/assets/bg1upscale.png)]"></div>
        {/* Video clips container */}
        <div className="flex flex-col space-y-16">
          {videos.map((video) => (
            <div key={video.id} className="flex items-center">
              <div className="mr-4 bg-gray-200 z-10 text-gray-800 px-4 py-1 rounded-full">{video.timestamp}</div>
              <div className="relative h-20 w-36  overflow-hidden rounded-xl border-4 border-white">
               
                <div className="absolute bottom-2 right-2 rounded-full bg-black bg-opacity-50 p-2">
                  
                </div>
              </div>
              <div className="mx-4 h-[2px] w-16 bg-[#d9d9d9]"></div>
              <div className="w-80 rounded-lg bg-[#d9d9d9] p-4">
                <h3 className="mb-2 font-medium text-black">Résumé :</h3>
                <p className="text-sm text-black">{video.summary}</p>
                <button className="mt-4 w-full rounded-md bg-[#a2a2a2] py-2 text-center text-sm">Download vidéo</button>
                <button
                  className={`mt-2 flex w-full items-center justify-between rounded-md py-2 px-4 text-sm ${
                    addedVideos.includes(video.id) ? "bg-green-500 text-white" : "bg-[#a2a2a2]"
                  }`}
                  onClick={() => handleAddToMontage(video.id)}
                >
                  <span>{addedVideos.includes(video.id) ? "Retirer du montage" : "Ajouter au montage"}</span>
                  {addedVideos.includes(video.id) ? (
                    <ArrowRight size={16} className="rotate-45" />
                  ) : (
                    <ArrowRight size={16} />
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Additional thumbnails in top right */}
      
      {addedVideos.length > 0 && (
        
        <div className="absolute right-12 top-0 py-4 px-4 z-10 rounded-b-3xl space-y-4 bg-[url(/assets/bg1upscale.png)]">

          {addedVideos.map((videoId) => {
            const video = videos.find((v) => v.id === videoId)
            return video ? (
              <div key={`added-${videoId}`} className="relative left-[-40px] overflow-hidden rounded-lg border-4 border-white">
               
              </div>
            ) : null
          })}
          <button className="mt-2 w-full rounded-md bg-[#a2a2a2] py-2 text-center text-xs z-50">Download vidéo</button>
        </div>
      )}
    </div>
  )

};


  

export default FileDetails;
