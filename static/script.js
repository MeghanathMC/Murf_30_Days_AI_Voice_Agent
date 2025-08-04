function sayHello() {
    alert("Hello - We are building an Voice AI Agent!");
}

async function generateAudio(){
    const textInput=document.getElementById("inputText").value;

   const audioPlayer= document.getElementById("audioPlayer");


    if(textInput.trim() === ""){
        alert("Please enter some text to generate audio");
        return;
    }

    const response= await fetch("/tts",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",

        },
        body:JSON.stringify({text:textInput})
    })

   const data=await response.json();


   if(data.audio_url && data.audio_url!=="Not Found"){
    audioPlayer.src=data.audio_url;
    audioPlayer.style.display="block";
    audioPlayer.play();
   
   }else{
    alert("Failed to generate audio");
   }


}