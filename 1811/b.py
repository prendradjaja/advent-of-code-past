# b_0.0.py is the naive solution, which is too slow:
#
#   # of corners
#     300 * 300
#   # of subgrid sizes
#     * 300
#   # of items to sum for each call to get_subgrid_sum()  (worst case)
#     * 300 * 300
#
#     = 2.43 * 10*12 i.e. runtime will be measured in hours.
#
#
# b_0.1.py is this idea:
# I can cache calls to get_subgrid_sum() and then: When calling e.g.
# get_subgrid_sum(grid, corner=(1, 2), size=4), reuse get_subgrid_sum(...,
# size=3) and just add the "extra items". This removes a factor of 300 from the
# runtime. This should run in minutes.
#
#
# TODO Implement this second optimization(?):
# My third thought is -- I think I can precompute all the 1xN and Nx1
# rectangles, then use that to compute the "extra items". Is that fast to do? If
# so, this removes another factor of 300 from the runtime, and should run in
# seconds.
#
#
# (Side note: What's that problem I've seen before that uses partial sums?)
