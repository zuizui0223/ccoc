import pytest

from causal_model.portability_adaptation_tradeoff import binary_portability_information_lower_bound, certify_portability_adaptation_tradeoff, exact_retention_update_frontier, full_binary_exterior_states


def test_exact_frontier_is_sharp_for_every_retention_split():
    m=4
    for k in range(m+1):
        cert=exact_retention_update_frontier(m,k)
        assert cert.verify()
        assert cert.retained_exterior_information_bits == pytest.approx(k)
        assert cert.update_conditional_entropy_bits == pytest.approx(m-k)
        assert cert.empirical_required_information_bits == pytest.approx(m)
        assert cert.empirical_tradeoff_slack_bits == pytest.approx(0.0)
        assert cert.minimum_update_entropy_from_contract_bits == pytest.approx(m-k)
        assert cert.minimum_update_state_count_from_contract == 2**(m-k)


def test_one_bit_update_saturates_approximate_two_bit_bound():
    states=full_binary_exterior_states(2)
    cert=certify_portability_adaptation_tradeoff(states,("c",)*4,tuple(s[0] for s in states),(lambda p:p[1],lambda p:0),(0.0,0.5))
    assert cert.verify()
    assert cert.empirical_coordinate_errors == pytest.approx((0.0,0.5))
    assert cert.retained_exterior_information_bits == pytest.approx(0.0)
    assert cert.update_conditional_entropy_bits == pytest.approx(1.0)
    assert cert.contract_required_information_bits == pytest.approx(1.0)
    assert cert.empirical_tradeoff_slack_bits == pytest.approx(0.0)


def test_retention_reduces_exact_update_one_for_one():
    cert=exact_retention_update_frontier(5,3)
    assert cert.retained_exterior_information_bits == pytest.approx(3.0)
    assert cert.update_conditional_entropy_bits == pytest.approx(2.0)
    assert cert.minimum_update_entropy_from_contract_bits == pytest.approx(2.0)


def test_declared_error_contract_fails_when_decoder_is_worse():
    states=full_binary_exterior_states(2)
    with pytest.raises(ValueError):
        certify_portability_adaptation_tradeoff(states,(0,)*4,tuple(s[0] for s in states),(lambda p:p[1],lambda p:0),(0.0,0.25))


def test_uniform_error_formula():
    from causal_model.approximate_addressability import binary_entropy
    m=7; error=0.1
    assert binary_portability_information_lower_bound((error,)*m) == pytest.approx(m*(1.0-binary_entropy(error)))


def test_invalid_frontier_parameters_fail_closed():
    with pytest.raises(ValueError): exact_retention_update_frontier(3,-1)
    with pytest.raises(ValueError): exact_retention_update_frontier(3,4)
    with pytest.raises(ValueError): full_binary_exterior_states(0)
