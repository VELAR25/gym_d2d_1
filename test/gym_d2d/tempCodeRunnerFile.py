def test_pl_constant_dB():
    ple = 2.0
    assert pl_constant_dB(2.0, ple) == approx(38,"it is running")  # pl_constant_dB(The carrier frequencies in Ghz., path loss exponent)
    assert pl_constant_dB(2.1, ple) == approx(38.892169116561746)
    assert pl_constant_dB(2.2, ple) == approx(39.2962368383275)
