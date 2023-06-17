*** Settings ***

Library    src.robot_framework.calcikeywords.CalculatorKeyworkds


*** Test Cases ***

Test Addition

    ${res}   Adding Two Numbers    5    6
    Should Be Equal     ${res}   ${11}

Test Substraction

    ${res}   Substract Two Numners        6   5
    Should Be Equal     ${res}   ${1}


Add 2 Nums
#    ${nums} =  ${5} + ${6}
    ${sum}=    Evaluate    ${5} + ${6}
    Log To Console     ${sum}