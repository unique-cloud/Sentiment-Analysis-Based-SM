class Micropost < ApplicationRecord
  has_many :combinations, dependent: :destroy
  has_many :tags, through: :combinations
  belongs_to :user
  default_scope -> { order(created_at: :desc) }
  validates :user_id, presence: true
  validates :content, presence: true, length: { maximum: 140 }

  def get_tag(tag)
    tags << tag
  end

end
