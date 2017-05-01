# Description
A prototype of an implementation of a content-sensitive image compression algorithm. FPEG detects faces in an image and compresses those regions less than the surrounding pixels. In theory the human visual cortex is more sensitive to compression artifacts on faces then surrounding context, therefore using higher compression in non-facial regions will lead to smaller images with comparable perceived quality.

See http://imgur.com/a/YT2TX for examples with filesizes.
