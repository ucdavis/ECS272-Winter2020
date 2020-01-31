import React, { useState, useContext } from "react";
import { useApolloClient, useQuery } from "@apollo/react-hooks";
import Select from "react-select";
import { gql } from "apollo-boost";

type SelectorProps = {
  data: object[];
  category?: string;
  target: string;
};

const query = gql`
  query @client {
    x {
      value
      __typename
    }
    y {
      value
      __typename
    }
    z {
      value
      __typename
    }
  }
`;

const Selector: React.FC<SelectorProps> = props => {
  const client = useApolloClient();
  const { data: state } = useQuery(query);

  const toggle = (option: any) => {
    client.writeData({
      data: {
        [props.target]: { value: option.value, __typename: "selection" }
      }
    });
    if (props.target === "x") {
      client.writeData({
        data: {
          y: { value: "", __typename: "selection" },
          z: { value: "", __typename: "selection" }
        }
      });
    }
  };

  let options =
    props.category !== undefined
      ? props.data
          .map(item => item[props.category! as keyof typeof props.data[0]])
          .reduce((prev: any, curr: any, index: any) => {
            return prev.indexOf(curr) > -1 ? prev : [...prev, curr];
          }, [])
          .sort((a: any, b: any) => (a > b ? 1 : -1))
          .map((item: any) => ({
            value: item,
            label: item
          }))
      : Object.keys(props.data[0])
          .filter(item => item !== "IncidntNum")
          .sort((a: any, b: any) => (a > b ? 1 : -1))
          .map(item => ({
            value: item,
            label: item
          }));

  if (options.length > 101) {
    options = options.slice(0, 100);
  }

  return (
    <React.Fragment>
      <Select
        isDisabled={props.target !== "x" && state.x.value === ""}
        options={options}
        onChange={toggle}
        value={
          state[props.target] === ""
            ? { value: null, label: null }
            : {
                value: state[props.target].value,
                label: state[props.target].value
              }
        }
      />
    </React.Fragment>
  );
};

export default Selector;
