require 'test_helper'

class TagTest < ActiveSupport::TestCase
  test "tag should be valid" do
    tag = Tag.new(name: "test")
    assert tag.valid?
  end

  test "name should be unique" do
    tag = Tag.new(name: "tag_1")
    assert_not tag.valid?
  end
end
