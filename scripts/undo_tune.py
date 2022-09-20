import attune

opa = "w2"
instr = attune.restore(
    opa, time="2022-08-19T19:45:47.205570-05:00"
)  # , can check date format of data with d.attrs["created"] on your data object
