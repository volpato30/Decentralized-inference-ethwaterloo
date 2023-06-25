import React from "react";

export function ModelRegistry({ modelRegisterFunc }) {
  return (
    <div>
      <h4>Register a new model</h4>
      <form
        onSubmit={(event) => {
          // This function just calls the transferTokens callback with the
          // form's data.
          event.preventDefault();
          // TODO: need to extract user input prompt here and pass to workers.
          const formData = new FormData(event.target);
          const url = formData.get("url");
          modelRegisterFunc(url);
        }}
      >
        <div className="form-group">
          <label>Model IPFS url</label>
          <input className="form-control" type="text" name="url" required />
        </div>
        <div className="form-group">
          <input className="btn btn-primary" type="submit" value="register" />
        </div>
      </form>
    </div>
  );
}
