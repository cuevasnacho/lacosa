import React from "react";
import { render } from "@testing-library/react";
import Carta from "./Carta";

it("renders without crashing", function () {
  render(<Carta />);
});
