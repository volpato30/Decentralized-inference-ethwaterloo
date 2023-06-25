import React from "react";

export function Pay({ payFunc }) {
  return (
    <div>
      <h4>Inference</h4>
      <form
        onSubmit={(event) => {
          // This function just calls the transferTokens callback with the
          // form's data.
          event.preventDefault();
          // TODO: need to extract user input prompt here and pass to workers.
          const formData = new FormData(event.target);
          const inputPrompt = formData.get("prompt");
          payFunc(inputPrompt);
        }}
      >
        <div className="form-group">
          <label>Input prompt</label>
          <input className="form-control" type="text" name="prompt" required />
        </div>
        <div className="form-group">
          <label>Model ID</label>
          <input
            className="form-control"
            type="number"
            step="1"
            name="modelId"
            placeholder="1"
            required
          />
        </div>
        <div className="form-group">
          <input className="btn btn-primary" type="submit" value="Inference" />
        </div>
      </form>
    </div>
  );
}
