import React from "react";

export function ResultImage(props) {
  const imageStr = 'data:image/png;base64,' + props.imageResult;
    return (
      <div>
        <img 
          src={imageStr} 
          alt="logo" 
        />
      </div>
    );
  }