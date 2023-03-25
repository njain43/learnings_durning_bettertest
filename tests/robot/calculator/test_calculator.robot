*** Settings ***

Library    src.robot.keywords.CalculatorKeyworkds


*** Test Cases ***

Test Addition

    ${res}   Adding Two Numbers    5    6
    Should Be Equal     ${res}   ${11}

Test Substraction

    ${res}   Substract Two Numners        6   5
    Should Be Equal     ${res}   ${1}