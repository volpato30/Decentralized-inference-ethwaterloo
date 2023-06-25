import React from "react";

export function Stake({ stakeFunc }) {
  return (
    <div>
      <h4>Stake</h4>
      <h6>by clicking the stake button, you will deposit 0.1 ETH into the protocol.</h6>
      <form
        onSubmit={(event) => {
          // This function just calls the transferTokens callback with the
          // form's data.
          event.preventDefault();
          stakeFunc();
        }}
      >
        <div className="form-group">
          <input className="btn btn-primary" type="submit" value="Stake" />
        </div>
      </form>
    </div>
  );
}
