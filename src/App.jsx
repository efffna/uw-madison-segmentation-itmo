import React, { useState, useEffect } from "react";
import "./App.css"

export default function App() {

    const upload_url = "http://127.0.0.1:8000/upload_files"
    const get_img_url = "http://127.0.0.1:8000/get_mask"
    
    const [uploadStatus, setUploadStatus] = useState(".")
    const [img, setImg] = useState();
    const [type, setType] = useState("upload");
 
    useEffect(() => {
        fetch(get_img_url)
            .then(res => res.json())
        fetchImage();
    }, [uploadStatus])

    const onImageChange = (event) => {
        if (event.target.files && event.target.files[0]) {
            sendImg(event.target.files)
        }
    }

    const sendImg = (files) => {
        let formData = new FormData()
        


        for (let i = 0; i < files.length; i++) {
            formData.append(`images[${i}]`, files[i])
        }


        const values = [...formData.entries()];
        
        console.log(values);

        fetch(upload_url, {
            method: "POST",
            body: formData,
            headers: {
                'Content-Type': 'multipart/form-data'}

        })
            .then(setUploadStatus(".."))
    }

    const fetchImage = async () => {
        const res = await fetch(get_img_url);
        const imageBlob = await res.blob();
        const imageObjectURL = URL.createObjectURL(imageBlob);
        setImg(imageObjectURL);
        setUploadStatus("...")
    };

    let content;

    switch (type) {
        default:
        case "upload":
            content = (
                <div>

                    <div className="title">
                        GI tract Image Segmentation
                    </div>

                    <div className="upload">
                        <div >
                        <div className="title2">
                            Upload image file for segmentation:
                    </div>
                        <input type="file" class="inputfile" onChange={onImageChange} multiple/>
                    </div>
                    </div>
                    <div className="show_image">
                        <button onClick={() => { setType("show_image") }}> GET MASKS </button>
                    </div>

                    <div className="uploadStatus">
                        {uploadStatus}
                    </div>
                    
                    <div className="mask">
                        
                    </div>

                </div>
            )
            break
        case "show_image":
                content = (
                    <div>
                        <div className="image">
                            <img src={get_img_url} alt="not image" />
                        </div>
                        
                        <div className="back">
                            <button onClick={() => { setType("upload") }}>BACK</button>
                        </div>
                    </div>
                )
                break
        
        case "mask":
                content = (
                    <div>
                        <section>
                        <ul class="main legend">
                            <li>
                                <em>Large Bowel</em>
                                </li>
                                <li>
                                <em>Small Bowe</em>
                                </li>
                                <li>
                                <em>Stomach</em>
                                </li>
                            </ul>
                        </section>
                        <div className="back">
                            <button onClick={() => { setType("upload") }}>Back</button>
                        </div>
                    </div>
                )
                break
        }

    return content
}