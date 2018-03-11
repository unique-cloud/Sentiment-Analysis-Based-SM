class Tag < ApplicationRecord
  has_many :combinations, dependent: :destroy
  has_many :microposts, through: :combinations
  has_many :users, through: :microposts
  before_save :downcase_name
  validates :name, presence: true, length: { maximum: 50 },
            uniqueness: { case_sensitive: false }

  def downcase_name
    name.downcase!
  end
end
