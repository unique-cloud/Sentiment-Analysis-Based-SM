# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

<<<<<<< HEAD
ActiveRecord::Schema.define(version: 20180225064624) do
=======
ActiveRecord::Schema.define(version: 20180225064921) do
>>>>>>> b4dce385e646c4552de668760fc90f81d9b7bcbb

  create_table "users", force: :cascade do |t|
    t.string "name"
    t.string "email"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "password_digest"
    t.string "remember_digest"
<<<<<<< HEAD
    t.boolean "admin", default: false
=======
    t.string "activation_digest"
    t.boolean "activated", default: false
    t.datetime "activated_at"
>>>>>>> b4dce385e646c4552de668760fc90f81d9b7bcbb
    t.index ["email"], name: "index_users_on_email", unique: true
  end

end
