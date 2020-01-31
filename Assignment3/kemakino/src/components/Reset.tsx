import React from "react";
import { Button } from "@material-ui/core";
import { useApolloClient } from "@apollo/react-hooks";

type Props = {};

const Reset: React.FC<Props> = (props: Props) => {
  const client = useApolloClient();
  const click = () => {
    client.writeData({
      data: {
        x: { value: "", __typename: "selection" },
        y: { value: "", __typename: "selection" },
        z: { value: "", __typename: "selection" },
        xt: { value: "", __typename: "selection" },
        zt: { value: "", __typename: "selection" }
      }
    });
  };

  return (
    <>
      <Button
        size={"large"}
        color={"primary"}
        variant={"contained"}
        onClick={click}
      >
        Reset
      </Button>
    </>
  );
};

export default Reset;
