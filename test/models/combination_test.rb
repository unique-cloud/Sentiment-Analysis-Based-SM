require 'test_helper'

class CombinationTest < ActiveSupport::TestCase

  def setup
    @combination = Combination.new(micropost_id: microposts(:orange).id,
                                   tag_id: tags(:tag_1).id )
  end

  test "should be vaild" do
    assert @combination.valid?
  end

  test "should require a micropost_id" do
    @combination.micropost_id = nil
    assert_not @combination.valid?
  end

  test "should require a tag_id" do
    @combination.tag_id = nil
    assert_not @combination.valid?
  end

end
