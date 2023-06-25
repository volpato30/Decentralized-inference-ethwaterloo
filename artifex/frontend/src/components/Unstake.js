import React from "react";

export function UnStake({ unstakeFunc }) {
  return (
    <div>
      <h4>UnStake</h4>
      <h6>by clicking the UnStake button, you will retrieve all your deposit & reward from the DI protocol.</h6>
      <form
        onSubmit={(event) => {
          // This function just calls the transferTokens callback with the
          // form's data.
          event.preventDefault();
          unstakeFunc();
        }}
      >
        <div className="form-group">
          <input className="btn btn-primary" type="submit" value="UnStake" />
        </div>
      </form>
    </div>
  );
}
