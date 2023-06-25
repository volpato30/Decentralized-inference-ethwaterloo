import React from "react";

export function ResultImage(props) {
  const imageStr = props.imageResult;
  console.log("imageStr", imageStr)
    return (
      <div>
        <img 
          src={imageStr} 
          alt="logo" 
        />
      </div>
    );
  }